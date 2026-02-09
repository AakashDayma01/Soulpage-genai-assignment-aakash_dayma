import os
import requests
from dotenv import load_dotenv
from ddgs import DDGS
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate

load_dotenv()

# Initialize LLM
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant", temperature=0)
memory = ConversationBufferMemory(memory_key="history", return_messages=True, input_key="input")
current_entity = None

# Small talk prompt
chat_prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""
        You are a conversational assistant.

        Rules:
        - Keep replies short
        - No explanations unless asked
        - Respond naturally

        Conversation:
        {history}

        User: {input}
        Assistant:
    """
)
conversation = ConversationChain(llm=llm, memory=memory, prompt=chat_prompt, verbose=False)

def detect_intent(text: str) -> str:
    prompt = f"""
        Classify the user message into ONE word only.

        Rules:
        - small_talk → greetings, wishes, casual chat, emotions
        - factual → asking for information or facts

        Message:
        {text}

        Answer only one word: small_talk or factual
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip().lower()

def extract_entity(text: str) -> str | None:
    prompt = f"""
        Extract the MAIN person or company name from the message.
        If none is mentioned, return NONE.

        Message:
        {text}

        Answer ONLY the name or NONE.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    result = response.content.strip()
    return None if result.upper() == "NONE" else result

def format_history():
    msgs = memory.load_memory_variables({})["history"]
    history_text = ""
    for i in range(len(msgs)):
        role = "User" if i % 2 == 0 else "Bot"
        history_text += f"{role}: {msgs[i].content}\n"
    return history_text.strip()

def rewrite_question(user_query: str, entity: str | None) -> str:
    if not entity:
        return user_query
    prompt = f"""
        Rewrite the question to be fully standalone using the context below.

        Context entity:
        {entity}

        User question:
        {user_query}

        Return ONLY the rewritten question.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

def free_search(query: str) -> str:
    snippets = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, backend="auto"):
                if r.get("body"):
                    snippets.append(r["body"])
                if len(snippets) >= 5:
                    break
    except:
        pass
    try:
        wiki_url = "https://en.wikipedia.org/w/api.php"
        params = {"action": "opensearch", "search": query, "limit": 3, "format": "json"}
        r = requests.get(wiki_url, params=params, timeout=10)
        if r.status_code == 200:
            snippets.extend(r.json()[2])
    except:
        pass
    return "\n".join(snippets) if snippets else "I do not know."

def verify_answer(user_query: str, llm_answer: str) -> str:
    snippets = free_search(user_query)
    if llm_answer.lower() in snippets.lower():
        return llm_answer
    else:
        prompt = f"""
            You are a factual assistant.

            Check the answer below against the information provided. 
            If the answer is correct, return it. If wrong, generate correct answer.

            LLM Answer:
            {llm_answer}

            Information:
            {snippets}

            Return ONLY the correct answer.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()

# ✅ This is the function that main.py will import
def get_bot_response(user_input: str) -> str:
    global current_entity

    intent = detect_intent(user_input)

    if intent == "small_talk":
        response = conversation.predict(input=user_input)
        return response

    # Factual flow
    entity = extract_entity(user_input)
    if entity:
        current_entity = entity

    rewritten = rewrite_question(user_input, current_entity)
    llm_answer_prompt = f"""
        Answer the question concisely and factually.

        Rules:
        - Do NOT include extra titles, nicknames, or historical roles.
        - Only provide the plain factual answer based on public information.

        Question: {rewritten}
    """
    llm_answer = llm.invoke([HumanMessage(content=llm_answer_prompt)]).content.strip()
    final_answer = verify_answer(rewritten, llm_answer)
    memory.save_context({"input": user_input}, {"output": final_answer})
    return final_answer



#Chat loop
if __name__ == "__main__":
    print("Conversational Knowledge Bot (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break

        intent = detect_intent(user_input)

        # Small Talk
        if intent == "small_talk":
            response = conversation.predict(input=user_input)
            print("Bot:", response)
            continue

        # Factual Flow
        entity = extract_entity(user_input)
        if entity:
            current_entity = entity

        # Rewrite question in context
        rewritten = rewrite_question(user_input, current_entity)

        # Let LLM answer first
        llm_answer_prompt = f"""
            Answer the question concisely and factually.

            Rules:
            - Do NOT include extra titles, nicknames, or historical roles.
            - Only provide the plain factual answer based on public information.

            Question: {rewritten}
        """
        llm_answer = llm.invoke([HumanMessage(content=llm_answer_prompt)]).content.strip()

        # Verify answer against search
        final_answer = verify_answer(rewritten, llm_answer)

        print("Bot:", final_answer)

        memory.save_context({"input": user_input}, {"output": final_answer})
