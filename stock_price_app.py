import pandas as pd  
import yfinance as yf
import streamlit as st   
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

# Setting up the app title and layout
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("💹Stock Market Analysis Dashboard")
st.markdown("""
            This app demonstrates real-time stock data visualization and analysis using:
            - **Python** for backend logic
            - **Streamlit** for UI components
            - **Plotly** for interactive visualizations
            - **Yahoo Finance API** for data fetching
            """)

@st.cache_data
def load_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url)
    return html[0]['Symbol'].astype(str).str.replace(r'\W', '', regex=True).tolist()

# Creating a sidebar for user inputs
with st.sidebar:
    st.header("User Inputs")
    
    ticker = st.selectbox(
        "Select stock ticker:",
        load_sp500_tickers(),
        index=0
    )
    date_range = st.select_slider(
        "Select date range:",
        options=['1M', '3M', '6M', '1Y', '5Y'],
        value='6M'
    )
    
# Fetching stock data using Yahoo Finance API
@st.cache_data
def get_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return stock, data

try:
    stock, data = get_stock_data(ticker, date_range)
    if data.empty:
        st.error("No data found for this ticker!")
        st.stop()
        
except:
    st.error("Failed to fetch data. Please check your input!")
    st.stop()
    
# Main dashboard layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Current Price", value=f"${data['Close'].iloc[-1]:.2f}")
with col2:
    st.metric(label="52 Week High", value=f"${stock.info['fiftyTwoWeekHigh']:.2f}")
with col3:
    st.metric(label="52 Week Low", value=f"${stock.info['fiftyTwoWeekLow']:.2f}")

# Creating charts that are interactive
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1, row_heights=[0.7, 0.3])

# Candlestick chart
fig.add_trace(go.Candlestick(x=data.index,
                             open=data['Open'],
                             high=data['High'],
                             low=data['Low'],
                             close=data['Close'],
                             name='Price'), row=1, col=1)

# Volume chart
fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'), row=2, col=1)

# Updating layout 
fig.update_layout(height=800, title=f"{ticker} Stock Analysis",
                  xaxis_rangeslider_visible=False,
                  hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)