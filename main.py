import streamlit as st
import yfinance as yf
import datetime

st.write("""
# Simple Stock Price App


""")

def valid_to_symbol(s):
    try:
        yf.Ticker(s).info
        return True
    except:
        return False

now = datetime.datetime.today()
symbol = st.text_input("Enter the Stock Symbol")

if symbol:
    if valid_to_symbol(symbol):
        st.success(f"{symbol} is a valid stock symbol")

        tickerData = yf.Ticker(symbol)
        tickerDF = tickerData.history(period="1d", start="2010-5-31", end=now)

        for column in tickerDF.columns:
            st.markdown(f"### 📉 {column} Over Time")
            st.line_chart(tickerDF[column])

    else:
        st.error(f"{symbol} is not a valid stock symbol")





