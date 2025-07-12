"""
Stock of the Day (SOTD) - A Flask web application that generates daily stock recommendations
by having AI discover and analyze promising small-cap stocks using current market data and news.
"""

import os
import logging
from typing import List, Dict, Optional
import requests
from flask import Flask, render_template, abort
from dotenv import load_dotenv
import yfinance as yf
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate required environment variables
if not NEWSAPI_KEY:
    raise ValueError("NEWSAPI_KEY environment variable is required")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# API configuration
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
OPENAI_MODEL = "gpt-4o-mini"


def get_news_headlines(ticker: str, max_articles: int = 3) -> List[str]:
    """
    Fetch recent news headlines for a given stock ticker.
    
    Args:
        ticker: Stock symbol to search for
        max_articles: Maximum number of articles to return
        
    Returns:
        List of news headlines
        
    Raises:
        requests.RequestException: If the API request fails
    """
    try:
        params = {
            "q": ticker,
            "sortBy": "publishedAt",
            "apiKey": NEWSAPI_KEY
        }
        
        response = requests.get(NEWS_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])[:max_articles]
        
        return [article["title"] for article in articles]
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch news for {ticker}: {e}")
        return []


def get_stock_price_data(ticker: str) -> Dict[str, Optional[float]]:
    """
    Fetch current stock price and daily change percentage.
    
    Args:
        ticker: Stock symbol to fetch data for
        
    Returns:
        Dictionary containing price and change percentage
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        current_price = info.get("regularMarketPrice")
        previous_close = info.get("regularMarketPreviousClose")
        
        change_percentage = None
        if current_price and previous_close and previous_close != 0:
            change_percentage = round(
                (current_price - previous_close) / previous_close * 100, 2
            )
        
        return {
            "price": current_price,
            "change_percentage": change_percentage
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch stock data for {ticker}: {e}")
        return {"price": None, "change_percentage": None}


def get_ai_stock_discovery() -> Optional[str]:
    """
    Have AI discover the single most promising small-cap stock.
    
    Returns:
        AI-generated recommendation for the top stock with reasoning
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a top stock analyst specializing in small-cap stocks. "
                              "Your job is to identify the single most promising small-cap stock "
                              "(market cap under $2B) that shows the highest potential for significant growth."
                },
                {
                    "role": "user",
                    "content": "Based on current market conditions, identify the ONE most promising small-cap stock "
                              "that you believe has the highest potential for growth in the near term. "
                              "Provide: 1) Stock symbol, 2) Company name, 3) Detailed reasoning why this is "
                              "your top pick. Focus on stocks with strong fundamentals, recent positive "
                              "developments, or emerging trends. Be specific and thorough in your analysis."
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Failed to get AI stock discovery: {e}")
        raise


def analyze_single_stock(stock_symbol: str) -> Optional[Dict]:
    """
    Analyze a single stock by fetching its current data and news.
    
    Args:
        stock_symbol: Stock symbol to analyze
        
    Returns:
        Dictionary containing analyzed stock data or None if failed
    """
    try:
        # Fetch stock price data
        price_data = get_stock_price_data(stock_symbol)
        
        # Fetch news headlines
        news_headlines = get_news_headlines(stock_symbol)
        
        return {
            "symbol": stock_symbol,
            "price": price_data["price"],
            "change_percentage": price_data["change_percentage"],
            "news": news_headlines
        }
        
    except Exception as e:
        logger.error(f"Failed to analyze stock {stock_symbol}: {e}")
        return None


def build_analysis_prompt(stock_data: Dict) -> str:
    """
    Build a prompt for AI analysis based on discovered stock data and news.
    
    Args:
        stock_data: Dictionary containing stock information
        
    Returns:
        Formatted prompt string for AI analysis
    """
    price_str = f"${stock_data['price']}" if stock_data['price'] else "N/A"
    change_str = f"{stock_data['change_percentage']}%" if stock_data['change_percentage'] is not None else "N/A"
    news_str = "; ".join(stock_data['news']) if stock_data['news'] else "No recent news"
    
    prompt = (
        f"You are a top stock analyst. Based on the following discovered small-cap stock with its "
        f"current price, daily change, and recent news headlines, provide a detailed analysis "
        f"of this stock's potential for significant growth:\n\n"
        f"Stock: {stock_data['symbol']}\n"
        f"Current Price: {price_str}\n"
        f"Daily Change: {change_str}\n"
        f"Recent News: {news_str}\n\n"
        f"Provide a comprehensive analysis including:\n"
        f"1. Why this stock shows promise\n"
        f"2. Key factors driving its potential\n"
        f"3. Risk considerations\n"
        f"4. Your overall recommendation"
    )
    
    return prompt


def get_ai_recommendation(prompt: str) -> Optional[str]:
    """
    Get AI recommendation using OpenAI API.
    
    Args:
        prompt: Analysis prompt to send to AI
        
    Returns:
        AI-generated recommendation text
        
    Raises:
        Exception: If the API request fails
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful stock analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Failed to get AI recommendation: {e}")
        raise


def extract_stock_symbol(ai_discovery: str) -> Optional[str]:
    """
    Extract the single stock symbol from AI discovery text.
    
    Args:
        ai_discovery: AI-generated text about the discovered stock
        
    Returns:
        Single stock symbol or None if not found
    """
    # Simple extraction - look for common stock symbol patterns
    import re
    # Look for 1-5 letter combinations that are likely stock symbols
    symbols = re.findall(r'\b[A-Z]{1,5}\b', ai_discovery)
    # Filter out common words that might be mistaken for symbols
    common_words = {'THE', 'AND', 'FOR', 'ARE', 'YOU', 'ALL', 'NEW', 'TOP', 'BEST', 'HIGH', 'LOW'}
    symbols = [s for s in symbols if s not in common_words and len(s) >= 2]
    return symbols[0] if symbols else None  # Return the first symbol found


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/stock")
def stock():
    """
    Generate and display the stock of the day recommendation using AI-discovered stocks.
    
    Returns:
        Rendered template with AI recommendation
        
    Raises:
        500: If there's an error generating the recommendation
    """
    try:
        # Step 1: Have AI discover promising stocks
        logger.info("Discovering promising stocks...")
        ai_discovery = get_ai_stock_discovery()
        
        if ai_discovery is None:
            abort(500, description="Failed to discover stocks")
        
        # Step 2: Extract stock symbol from AI discovery
        stock_symbol = extract_stock_symbol(ai_discovery)
        
        if not stock_symbol:
            abort(500, description="Failed to discover any stocks")
        
        logger.info(f"Discovered stock: {stock_symbol}")
        
        # Step 3: Analyze the single discovered stock
        stock_data = analyze_single_stock(stock_symbol)
        
        if not stock_data:
            abort(500, description="Failed to analyze the discovered stock")
        
        # Step 4: Build analysis prompt
        analysis_prompt = build_analysis_prompt(stock_data)
        
        # Step 5: Get AI recommendation
        ai_recommendation = get_ai_recommendation(analysis_prompt)
        
        if ai_recommendation is None:
            abort(500, description="Failed to get AI recommendation")
        
        # Combine discovery and recommendation
        full_analysis = f"AI Stock Discovery:\n{ai_discovery}\n\n" \
                       f"Detailed Analysis:\n{ai_recommendation}"
        
        return render_template("stock.html", ai_pick=full_analysis)
        
    except Exception as e:
        logger.error(f"Error generating stock recommendation: {e}")
        abort(500, description="Failed to generate stock recommendation")


if __name__ == "__main__":
    app.run(debug=True)
