import yfinance as yf
GLOBAL_TICKERS = {
    "tesla": "TSLA", "microsoft": "MSFT", "apple": "AAPL", "google": "GOOGL", "amazon": "AMZN",
    "facebook": "META", "netflix": "NFLX", "nike": "NKE", "coca-cola": "KO", "pepsi": "PEP",
    "ibm": "IBM", "intel": "INTC", "nvidia": "NVDA", "paypal": "PYPL", "disney": "DIS",
    "samsung": "005930.KS", "hyundai": "005380.KS", "lg electronics": "066570.KQ",
    "toyota": "7203.T", "sony": "6758.T", "mitsubishi": "8058.T",
    "alibaba": "BABA", "baidu": "BIDU", "tencent": "0700.HK", "jd.com": "9618.HK",
    "infosys": "INFY", "tata motors": "TTM", "wipro": "WIT", "hdfc bank": "HDB",
    "reliance": "RELIANCE.NS", "icici bank": "IBN",
    "siemens": "SIE.DE", "adidas": "ADS.DE", "bmw": "BMW.DE", "allianz": "ALV.DE",
    "hsbc": "HSBA.L", "bp": "BP.L", "vodafone": "VOD.L",
    "shopify": "SHOP.TO", "td bank": "TD.TO",
    "commonwealth bank": "CBA.AX", "banco westpac": "WBC.AX"
}

def StockPerformanceTool(company_name: str) -> str:
    """Fetch stock price and market cap for a company"""
    ticker = GLOBAL_TICKERS.get(company_name.lower())
    if not ticker:
        try:
            search_results = yf.Tickers(company_name)
            for t in search_results.tickers:
                info = t.info
                if info.get("shortName") and company_name.lower() in info["shortName"].lower():
                    ticker = t.ticker
                    break
            if not ticker and search_results.tickers:
                ticker = search_results.tickers[0].ticker
        except Exception:
            pass

    if ticker:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("regularMarketPrice")
            currency = info.get("currency", "USD")
            market_cap = info.get("marketCap", "N/A")
            if price:
                return f"Stock Price ({ticker}): {price} {currency}\nMarket Cap: {market_cap}"
            return f"Stock data not found for {ticker}"
        except Exception as e:
            return f"Error fetching stock data: {str(e)}"
    return "Ticker not found. Unable to fetch stock data."
