# pages/1_Stock_Analysis.py
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from utils import plotly_figures as pf

st.set_page_config(page_title="Stock Analysis", layout="wide")
st.title("Stock Technical Analysis")

# --- User Input ---
col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Enter Stock Ticker", "TSLA")
with col2:
    start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=365))
with col3:
    end_date = st.date_input("End Date", datetime.date.today())

# --- Fetch Data ---
try:
    stock_info = yf.Ticker(ticker).info
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    
    # --- Display Company Info ---
    st.subheader(f"{ticker} - {stock_info.get('longName', 'N/A')}")
    st.markdown(f"**Sector:** {stock_info.get('sector', 'N/A')} | **Industry:** {stock_info.get('industry', 'N/A')} | **Website:** {stock_info.get('website', 'N/A')}")
    with st.expander("View Company Summary"):
        st.write(stock_info.get('longBusinessSummary', 'No summary available.'))

    # --- Key Metrics ---
    st.subheader("Key Metrics")
    col_a, col_b = st.columns(2)
    with col_a:
        df1 = pd.DataFrame({
            "Metric": ["Market Cap", "Beta", "Trailing EPS", "Trailing PE"],
            "Value": [stock_info.get('marketCap', 'N/A'), stock_info.get('beta', 'N/A'), stock_info.get('trailingEps', 'N/A'), stock_info.get('trailingPE', 'N/A')]
        }).set_index("Metric")
        st.plotly_chart(pf.plotly_table(df1), use_container_width=True)
    with col_b:
        df2 = pd.DataFrame({
            "Metric": ["Forward PE", "Price to Book", "52 Week High", "52 Week Low"],
            "Value": [stock_info.get('forwardPE', 'N/A'), stock_info.get('priceToBook', 'N/A'), stock_info.get('fiftyTwoWeekHigh', 'N/A'), stock_info.get('fiftyTwoWeekLow', 'N/A')]
        }).set_index("Metric")
        st.plotly_chart(pf.plotly_table(df2), use_container_width=True)

    # --- Interactive Chart ---
    st.subheader("Interactive Stock Chart")
    
    # Time period buttons
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    periods = {'5d': c1, '1m': c2, '6m': c3, '1y': c4, '5y': c5, 'max': c6}
    selected_period = '1y' # Default
    for period, col in periods.items():
        if col.button(period, use_container_width=True):
            selected_period = period

    # Chart controls
    ctrl1, ctrl2 = st.columns(2)
    chart_type = ctrl1.selectbox("Chart Type", ["Candlestick", "Line"])
    
    indicator_options = ["RSI", "MACD"]
    if chart_type == "Line":
        indicator_options.append("Moving Average")
    
    indicator = ctrl2.selectbox("Indicator", indicator_options)
    
    # --- Plotting logic ---
    if chart_type == "Candlestick":
        if indicator == "RSI":
            fig = pf.rsi_chart(data, selected_period)
        else: # MACD
            fig = pf.macd_chart(data, selected_period)
    else: # Line Chart
        if indicator == "Moving Average":
            fig = pf.moving_average_chart(data, selected_period)
        else: # RSI or MACD on a line chart would be less standard
            st.info("Line chart shows Close Price. Select 'Moving Average' for an overlay.")
            data_filtered = pf.filter_data(data, selected_period)
            fig = go.Figure(go.Scatter(x=data_filtered['Date'], y=data_filtered['Close'], mode='lines', name='Close Price'))
            fig.update_layout(title="Close Price Chart")

    st.plotly_chart(fig, use_container_width=True)

    # --- Historical Data Table ---
    st.subheader("Historical Data (Last 10 Days)")
    last_10_days = data.tail(10).round(2).sort_index(ascending=False)
    st.dataframe(last_10_days, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Failed to fetch data for {ticker}. Please check the ticker symbol and try again.")
    st.error(f"Details: {e}")