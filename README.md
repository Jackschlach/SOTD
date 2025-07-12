# 📈 Stock of the Day (SOTD)

An AI-powered Flask web application that generates daily stock recommendations by discovering and analyzing promising small-cap stocks using real-time market data and news.

## 🚀 Features

- **🤖 AI-Driven Discovery**: Automatically finds the most promising small-cap stocks based on current market conditions
- **📊 Real-time Data**: Fetches live price data from Yahoo Finance and recent news from NewsAPI
- **💡 Smart Analysis**: Provides comprehensive analysis with detailed reasoning, risk assessment, and recommendations
- **🎨 Modern UI**: Beautiful, responsive web interface with professional styling
- **📱 Mobile-Friendly**: Optimized for all devices and screen sizes

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI**: OpenAI GPT-4o-mini
- **Stock Data**: Yahoo Finance (yfinance)
- **News API**: NewsAPI.org
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern gradients and animations

## 📋 Prerequisites

- Python 3.8+
- NewsAPI key (free at https://newsapi.org/register)
- OpenAI API key (from https://platform.openai.com/api-keys)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-of-the-day.git
   cd stock-of-the-day
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   NEWSAPI_KEY=your_newsapi_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   python3 App.py
   ```

5. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 📁 Project Structure

```
SOTD/
├── App.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── templates/
    ├── index.html       # Homepage template
    └── stock.html       # Stock recommendation template
```

## 🔧 Configuration

### Environment Variables

- `NEWSAPI_KEY`: Your NewsAPI key for fetching stock news
- `OPENAI_API_KEY`: Your OpenAI API key for AI analysis

### API Configuration

The application uses:
- **NewsAPI**: For fetching recent news headlines about stocks
- **OpenAI GPT-4o-mini**: For AI-driven stock discovery and analysis
- **Yahoo Finance**: For real-time stock price data

## 🎯 How It Works

1. **AI Discovery**: The AI identifies the single most promising small-cap stock based on current market conditions
2. **Data Collection**: Fetches real-time price data and recent news for the discovered stock
3. **Analysis**: AI provides comprehensive analysis including:
   - Why the stock shows promise
   - Key factors driving potential
   - Risk considerations
   - Overall recommendation
4. **Presentation**: Displays results in a clean, professional web interface

## 🎨 Features

### Homepage (`/`)
- Modern, responsive design with gradient background
- Feature highlights explaining AI capabilities
- Smooth animations and hover effects
- Mobile-friendly layout

### Stock Recommendation Page (`/stock`)
- Professional card-based layout
- Clean display of AI analysis with proper formatting
- Important disclaimer for financial advice
- Refresh button to get new recommendations
- Responsive design for all devices

## ⚠️ Important Disclaimer

This application is for informational purposes only and should not be considered as financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NewsAPI](https://newsapi.org/) for providing stock news data
- [OpenAI](https://openai.com/) for AI analysis capabilities
- [Yahoo Finance](https://finance.yahoo.com/) for real-time stock data
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

**Made with ❤️ and AI** 