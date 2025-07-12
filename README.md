# Stock of the Day (SOTD)

Stock of the Day (SOTD) is a Flask web application that uses AI to identify and recommend a promising small-cap stock each day. The app fetches real-time price data and news, then leverages OpenAI to select and analyze a stock, providing a clear summary and reasoning in your browser.

## Overview
- **Discovery**: The app prompts OpenAI to select the single most promising small-cap stock (market cap under $2B) based on current market conditions.
- **Data Collection**: It retrieves the latest price and news headlines for the selected stock.
- **Analysis**: OpenAI provides a detailed explanation of why the stock was chosen, including key factors and potential risks.
- **Web Interface**: Results are presented in a clean, responsive web UI.

## Technology
- **Backend**: Python, Flask
- **AI**: OpenAI GPT-4o-mini
- **Market Data**: Yahoo Finance (yfinance)
- **News**: NewsAPI
- **Frontend**: HTML, CSS

## Getting Started
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
3. **Configure API keys** in a `.env` file:
   ```env
   NEWSAPI_KEY=your_newsapi_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. **Run the application**:
   ```bash
   python3 App.py
   ```
5. **Open your browser** to [http://localhost:5000](http://localhost:5000)

## Purpose
SOTD is designed to provide a simple, automated way to surface a new small-cap stock idea each day, with transparent AI-generated reasoning. It is intended for informational and educational use only.

---

**Disclaimer:** This application does not provide financial advice. Always conduct your own research before making investment decisions. 