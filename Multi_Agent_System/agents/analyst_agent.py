from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from utils.helpers import enforce_english

analyst_prompt_template = """
You are a professional financial data analyst specialized in stock market information.
You are given the following data about a company, including stock price, market cap, and latest news:

{data}

Your task:
1. Summarize the stock performance.
2. Highlight key trends or insights from the news.
3. Mention any potential risk factors.
4. Be concise, clear, and professional.
5. Respond ONLY in English.
"""
analyst_prompt = ChatPromptTemplate.from_template(analyst_prompt_template)

def AnalystAgent(agent1_data: str, llm_analyst) -> str:
    """Generate insights, summary, and risks in English"""
    sanitized_data = enforce_english(agent1_data)
    input_text = analyst_prompt.format(data=sanitized_data)
    response = llm_analyst([HumanMessage(content=input_text)])
    return response.content
