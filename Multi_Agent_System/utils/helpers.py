import re
from rapidfuzz import process

def enforce_english(text: str) -> str:
    """Forces Output of bot into English"""
    if not text:
        return ""
    return re.sub(r'[^\x00-\x7F]+', ' ', text)

def extract_company_fuzzy(user_query: str, threshold: int = 70) -> str:
    """Identify Spelling Mistack from Company name"""
    user_query_lower = user_query.lower()
    from services.stock_service import GLOBAL_TICKERS
    choices = list(GLOBAL_TICKERS.keys())
    match, score, _ = process.extractOne(user_query_lower, choices)
    if score >= threshold:
        return match
    return None
