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
        index=0,
        key="main_ticker_selector"  # Unique identifier
    )
    date_range = st.select_slider(
        "Select date range:",
        options=['1M', '3M', '6M', '1Y', '5Y'],
        value='6M',
        key="date_range_slider"  # Unique identifier
    )
    
# Fetching stock data using Yahoo Finance API
@st.cache_data
def get_historical_data(ticker, period):
    period_mapping = {
        '1M': '1mo',
        '3M': '3mo',
        '6M': '6mo',
        '1Y': '1y',
        '5Y': '5y'
    }
    try:
        return yf.Ticker(ticker).history(period=period_mapping.get(period, '6mo'))
    except Exception as e:
        st.error(f"Data fetch error: {str(e)}")
        return pd.DataFrame()

def get_company_info(ticker):
    try:
        return yf.Ticker(ticker).info
    except:
        return {}

with st.sidebar:
    st.header("User Inputs")
    ticker_list = load_sp500_tickers()
    ticker = st.selectbox("Select stock ticker:", ticker_list, index=0)
    date_range = st.select_slider("Date range:", ['1M', '3M', '6M', '1Y', '5Y'], '6M')

try:
    data = get_historical_data(ticker, date_range)
    company_info = get_company_info(ticker)
    
    if data.empty:
        st.error(f"No data found for {ticker}!")
        st.stop()
except Exception as e:
    st.error(f"Application error: {str(e)}")
    st.stop()
    
# Main dashboard layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Current Price", value=f"${data['Close'].iloc[-1]:.2f}")
with col2:
    high = company_info.get('fiftyTwoWeekHigh', 'N/A')
    st.metric(label="52 Week High", value=f"${high:.2f}" if isinstance(high, float) else high)
with col3:
    low = company_info.get('fiftyTwoWeekLow', 'N/A')
    st.metric(label="52 Week Low", value=f"${low:.2f}" if isinstance(low, float) else low)

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