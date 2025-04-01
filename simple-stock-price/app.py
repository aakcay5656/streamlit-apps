import streamlit as st
import yfinance as yf
import datetime
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Stock Price Tracker",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #00FF88;
        text-align: center;
    }
    .subtitle {
        font-size: 20px;
        color: #888888;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<p class="big-font">📈 Stock Price Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track real-time stock prices and historical data</p>', unsafe_allow_html=True)

def valid_to_symbol(s):
    try:
        yf.Ticker(s).info
        return True
    except:
        return False

# Create columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL, MSFT)", 
                          help="Enter the stock symbol you want to analyze")

now = datetime.datetime.today()

if symbol:
    symbol = symbol.upper()
    if valid_to_symbol(symbol):
        st.success(f"✅ {symbol} is a valid stock symbol")
        
        # Get stock data
        tickerData = yf.Ticker(symbol)
        company_info = tickerData.info
        
        # Display company info in the sidebar
        with st.sidebar:
            st.image(company_info.get('logo_url', ''), width=100)
            st.header(company_info.get('longName', symbol))
            st.write(f"Sector: {company_info.get('sector', 'N/A')}")
            st.write(f"Industry: {company_info.get('industry', 'N/A')}")
            
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.date(2010, 5, 31))
        with col2:
            end_date = st.date_input("End Date", now)

        # Get historical data
        tickerDF = tickerData.history(period="1d", start=start_date, end=end_date)
        
        # Display stock price chart
        st.subheader("Stock Price History")
        st.line_chart(tickerDF.Close, use_container_width=True)
        
        # Display volume chart
        st.subheader("Trading Volume")
        st.bar_chart(tickerDF.Volume, use_container_width=True)
        
        # Display key statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"${tickerDF.Close[-1]:.2f}", 
                     f"{((tickerDF.Close[-1] - tickerDF.Close[-2])/tickerDF.Close[-2]*100):.2f}%")
        with col2:
            st.metric("Market Cap", f"${company_info.get('marketCap')/1e9:.2f}B")
        with col3:
            st.metric("52 Week High", f"${company_info.get('fiftyTwoWeekHigh', 0):.2f}")
            
    else:
        st.error(f"❌ {symbol} is not a valid stock symbol")
else:
    # Default view with sample data
    default_symbol = "AAPL"
    tickerData = yf.Ticker(default_symbol)
    tickerDF = tickerData.history(period="1d", start="2010-5-31", end=now)
    
    st.info("👆 Enter a stock symbol above to begin analysis")
    st.subheader(f"Sample Data: {default_symbol} Stock Price History")
    st.line_chart(tickerDF.Close, use_container_width=True)
