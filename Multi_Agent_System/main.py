from utils.helpers import enforce_english, extract_company_fuzzy
from utils.formatting import heading, subheading, bullet, numbered,markdown_to_console_bold, human_readable_number


# detect stock-related query
def is_stock_query(user_input: str):
    """Identifies whether the query is stock and company news related or a general query."""
    return extract_company_fuzzy(user_input)

# collect stock + news data
def collect_stock_and_news(company_name, llm_collector):
    """Colletcts News And Stocks details of the company"""
    from agents.data_collector_agent import DataCollectorAgent

    collected = DataCollectorAgent(company_name, llm_collector)

    stock_data = collected.get("stock_data", "")
    news_data = enforce_english(collected.get("news", ""))

    return stock_data, news_data

# format stock data
def format_stock_data(stock_raw: str):
    formatted = []

    for line in stock_raw.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)

            if "Market Cap" in key:
                value = human_readable_number(value.strip())

            formatted.append(bullet(f"{key.strip()}: {value.strip()}"))
        else:
            formatted.append(line)

    return "\n".join(formatted)

# format news data
def format_news_data(news_raw: str):
    formatted = []

    for line in news_raw.split("\n"):
        if line.startswith("-"):
            formatted.append(bullet(line[1:].strip()))
        else:
            formatted.append(line)

    return "\n".join(formatted)

# analyst reasoning
def run_analyst(stock_raw, news_raw, llm_analyst):
    from agents.analyst_agent import AnalystAgent

    if "not found" in stock_raw.lower():
        return "No stock data available. Showing news only."

    try:
        analysis = AnalystAgent(f"{stock_raw}\n\n{news_raw}", llm_analyst)

        formatted_lines = []
        for line in analysis.split("\n"):
            if line and line[0].isdigit() and "." in line:
                num, text = line.split(".", 1)
                formatted_lines.append(
                    numbered(num, markdown_to_console_bold(text.strip()))
                )
            else:
                formatted_lines.append(markdown_to_console_bold(line))

        return "\n".join(formatted_lines)

    except Exception as e:
        return f"Failed to analyze data: {str(e)}"

#Orchastrator
def Orchestrator(user_input: str, llm_analyst=None, llm_collector=None, llm_general=None):
    company_name = is_stock_query(user_input)

    # Check Stock Query or General Query
    if company_name:
        stock_raw, news_raw = collect_stock_and_news(company_name, llm_collector)

        stock_formatted = format_stock_data(stock_raw)
        news_formatted = format_news_data(news_raw)

        analyst_output = run_analyst(stock_raw, news_raw, llm_analyst)

        return (
            heading("📊 DATA COLLECTOR RESULT") + "\n" +
            subheading("Stock & News Data") + "\n" +
            stock_formatted + "\n\n" +
            news_formatted + "\n\n" +
            heading("📈 ANALYST INSIGHTS") + "\n" +
            analyst_output
        )

    #General Query
    else:
        if llm_general is None:
            raise ValueError("llm_general must be provided")

        from agents.general_chat_agent import GeneralChatAgent
        return (
            heading("💬 GENERAL CHAT RESPONSE") + "\n" +
            GeneralChatAgent(user_input, llm_general)
        )

if __name__ == "__main__":
    from langchain_groq import ChatGroq
    from dotenv import load_dotenv
    import os

    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    llm_collector = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant", temperature=0)
    llm_analyst = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant", temperature=0)
    llm_general = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant", temperature=0.7)

    print("\n=== Two-Agent System: Data Collector + Analyst ===")

    while True:
        query = input("\nEnter company name or query (or 'exit'): ").strip()
        if query.lower() == "exit":
            break

        result = Orchestrator(query, llm_analyst, llm_collector, llm_general)
        print("\n" + result)
