# Conversational Knowledge Bot

A LangChain-powered conversational bot that remembers conversations, searches external data sources, and provides context-aware, factual answers.

# Features

✅ Full conversation memory using LangChain
✅ Intent detection: small talk vs factual queries
✅ Hybrid search: DuckDuckGo + Wikipedia
✅ Fact verification before answering
✅ Responsive Tkinter GUI with dynamic bubbles
✅ Groq LLM integration for fast answers

# Architecture

1. bot_logic.py — Handles LLM, memory, intent detection, search, and fact verification

2. main.py — Tkinter GUI with scrollable canvas and responsive bubbles

3. Search Pipeline — Extract entities, rewrite questions, search DuckDuckGo & Wikipedia, verify answers

4. Data Flow:

User Input
    ↓
detect_intent()
    ├─→ small_talk → ConversationChain.predict() → Memory Save
    └─→ factual:
        ├→ extract_entity()
        ├→ rewrite_question()
        ├→ free_search() [DuckDuckGo + Wikipedia]
        ├→ LLM Answer Generation
        ├→ verify_answer()
        └→ Memory Save + Display

# Setup
1. Prerequisites

Python 3.9+

Installation

2. Clone the repository:

git clone https://github.com/yourusername/conversational-knowledge-bot.git
cd conversational-knowledge-bot


# Create a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate


# Install dependencies:

1. pip install -r requirements.txt

2. API Key Setup (Preconfigured for Submission)

3. Your Groq API key is already included in .env for immediate testing

You can run the project immediately

# Note: This key is for evaluation purposes only.

# Running the Bot
# GUI Mode
python main.py


# Type messages and press Enter or click Send

# CLI Mode
python bot_logic.py


# Test the bot logic without GUI

Example Chat

Small Talk → Factual Question

You: Hi there!
Bot: Hello! How can I help you today?

You: Who is the CEO of OpenAI?
Bot: Sam Altman is the CEO of OpenAI. He founded OpenAI in 2015...


# Fact Verification

You: What is Python?
Bot: Python is a high-level programming language created by Guido van Rossum in 1989...

# Configuration

LLM model: bot_logic.py → model_name

Available Groq Models:

llama-3.1-8b-instant (fast)

llama-3.1-70b-versatile (larger)

mixtral-8x7b-32768 (very fast)

# Requirements
langchain>=0.1.0
langchain-groq>=0.1.0
requests>=2.31.0
python-dotenv>=1.0.0
duckduckgo-search>=3.9.0
tk>=0.1.0

# Troubleshooting

ModuleNotFoundError: Run pip install -r requirements.txt

No search results: Check internet connection and rephrase queries

GUI issues: Resize window after sending the first message

Slow response: Groq API free tier may have rate limits