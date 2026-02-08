# StockBot — Financial Chat Assistant

StockBot is a Python project that fetches real-time stock data and company news, then generates AI-powered market analysis. Works with any publicly listed company worldwide.

# Key Features:

1.  Chat GUI interface (chat_gui.py)

2.  Real-time stock data from YahuFinance API 

3.  Latest company news via NewsAPI

4.  AI-driven insights using Groq LLM


# Requirements

Python 3.10+

# Dependencies (see requirements.txt for exact versions):

python-dotenv — Load environment variables

requests — HTTP requests

yfinance — Stock data fetching

rapidfuzz — Fuzzy company name matching

langchain-groq — Groq LLM integration

langchain — LLM framework

#  Setup
1. Clone Project Folder
cd Project_for_internship

2. Create & Activate Virtual Environment

# Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1


# Linux / Mac:

python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. API Keys (Preconfigured for Submission)

.env file is included with Groq and NewsAPI keys for immediate use

# No setup required — ready for evaluation

5. Network Requirements

Ensure HTTPS access for:

api.groq.com (Groq LLM)

query1.finance.yahoo.com (Yahoo Finance)

newsapi.org (NewsAPI)

#  Architecture Overview
Folder Structure
Project_for_internship/
├── chat_gui.py                 # Tkinter GUI
├── main.py                     # CLI / Orchestrator
├── requirements.txt
├── .env                        # API keys (preconfigured)
├── agents2/                    # Agent modules
│   ├── data_collector_agent.py
│   ├── analyst_agent.py
│   └── general_chat_agent.py
├── services/                   # Data fetchers
│   ├── stock_service.py
│   └── news_service.py
└── utils/                      # Helpers
    ├── helpers.py
    └── formatting.py

# Media Samples

This project includes example media files (an image and a short demo video) stored under the `Project_Images_and_videos` folder:

- Image: Project_Images_and_videos/project_Images/image.png
- Video: Project_Images_and_videos/project_Images/Project_video/StockBot Chat 2026-02-08 17-05-09.mp4

To preview these locally, open the files in your file explorer or play the MP4 with your preferred media player. If you plan to publish the repository on GitHub, consider using Git LFS for large binary files or hosting the media externally to avoid bloating the repo.

# Component Roles
# Component	| Purpose
chat_gui.py	Launches the GUI chat interface
main.py	CLI / Orchestrator for queries
data_collector_agent.py	Fetches stock & news data
analyst_agent.py	Generates AI analysis using Groq LLM
general_chat_agent.py	Handles general queries
stock_service.py	Retrieves stock data dynamically
news_service.py	Fetches latest news
helpers.py	Input validation & fuzzy matching
formatting.py	Console text formatting
#  How It Works

1. User Input — Type a company name, ticker, or question in GUI/CLI.

2. Routing — Orchestrator detects stock vs general query.

3. Stock Queries — Collects:

4. Stock info: price, market cap, currency, country, industry

5. Latest news (5 articles)

6. AI insights generated via Groq LLM

7. General Queries — Handled by LLM directly.

8. Output Display — GUI shows chat bubbles; CLI prints formatted results.

#  Running the Application
1. GUI Mode (Recommended)
python chat_gui.py

Green bubbles = user messages

White bubbles = bot responses

2. CLI Mode (For Testing)
python main.py

Example Interaction:

Enter company or query: Tesla
📊 STOCK DATA
Price: $245.30 USD
Market Cap: $800.50B
...

📈 AI ANALYSIS
• Strong quarterly growth
• News shows market confidence
• Watch: Competition, regulations

#  Usage Examples
Stock Query

Input: Tesla
Output: Stock data + latest news + AI insights

Indian Stock

Input: Infosys
Output: Price, market cap, exchange info

Ticker Symbol

Input: AAPL
Output: Works like company name

General Query

Input: What is the stock market?
Output: LLM-generated explanation