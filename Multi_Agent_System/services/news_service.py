import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

def CompanyNewsTool(company_name: str, max_results: int = 5) -> str:
    """Fetch latest news for a company using NewsAPI"""
    try:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={company_name}&sortBy=publishedAt&"
            f"language=en&apiKey={NEWSAPI_KEY}&pageSize={max_results}"
        )
        res = requests.get(url).json()
        if res.get("status") != "ok" or not res.get("articles"):
            return "No recent news found."
        news_list = [f"- {a['title']} ({a['source']['name']})" for a in res["articles"]]
        return "Latest News (English):\n" + "\n".join(news_list)
    except Exception as e:
        return f"Error fetching news: {str(e)}"
