import pandas as pd 
import yfinance as yf
import streamlit as st 

st.write("""
    # Stock Price App
    
    Shown are the stock closing price and volume of Nasdaq
""")

# Defining the ticker symbol
ticker_symbol = 'GOOGL'

# Getting data from the ticker symbol
ticker_data = yf.Ticker(ticker_symbol)

# Getting historical prices for the ticker
ticker_period = ticker_data.history(period='1d', start='2010-5-31', end='2020-5-31')

st.line_chart(ticker_period.Close)
st.line_chart(ticker_period.Volume)
