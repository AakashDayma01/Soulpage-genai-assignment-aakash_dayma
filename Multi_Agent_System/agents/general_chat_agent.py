from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

def GeneralChatAgent(user_input: str, llm_general: ChatGroq) -> str:
    """
    General-purpose chat agent for non-stock queries.
    user_input: the question from user
    llm_general: ChatGroq instance
    """
    prompt = f"""
    You are a friendly, helpful assistant.
    Respond clearly, concisely, and professionally.
    Answer only in English.

    User's question: "{user_input}"
    """
    response = llm_general([HumanMessage(content=prompt)])
    return response.content
