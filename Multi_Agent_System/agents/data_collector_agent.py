from services.stock_service import StockPerformanceTool
from services.news_service import CompanyNewsTool

def DataCollectorAgent(user_query: str, llm_collector) -> dict:
    """LLM-based agent that decides and fetches data using tools"""
    stock_info = StockPerformanceTool(user_query)
    news_info = CompanyNewsTool(user_query)
    return {
        "company": user_query.strip(),
        "stock_data": stock_info,
        "news": news_info
    }
