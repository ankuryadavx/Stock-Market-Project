# pages/3_CAPM_Analysis.py

import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import datetime

# --- Helper Functions (specific to this page) ---

def calculate_beta_alpha(stock_returns, market_returns):
    """Calculates Beta and Alpha using linear regression."""
    beta, alpha = np.polyfit(market_returns, stock_returns, deg=1)
    return beta, alpha

def normalize_prices(df):
    """Normalizes prices to show growth of $1."""
    return df / df.iloc[0]

# --- Page Configuration ---
st.set_page_config(page_title="CAPM Analysis", layout="wide")
st.title("CAPM Analysis: Beta & Expected Return")
st.markdown("Compare stocks against the market (S&P 500) to evaluate risk and expected returns.")

# --- User Input ---
col1, col2 = st.columns([3, 1]) # Give more space to the stock selector
with col1:
    stocks_list = st.multiselect(
        "Choose stocks to compare",
        ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'),
        ['TSLA', 'AAPL', 'MSFT', 'GOOGL']
    )
with col2:
    years = st.number_input("Number of years", 1, 10, 5)

# --- Main Logic ---
try:
    # --- Data Download ---
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365.25 * years)

    # Download data for selected stocks and the S&P 500 market index
    all_tickers = stocks_list + ['^GSPC']
    data = yf.download(all_tickers, start=start_date, end=end_date)
    close_prices = data['Close'].rename(columns={'^GSPC': 'S&P 500'})

    # --- Calculations ---
    daily_returns = close_prices.pct_change().dropna()
    market_returns = daily_returns['S&P 500']
    
    # Prepare DataFrame for results
    results_data = []
    for stock in stocks_list:
        stock_returns = daily_returns[stock]
        beta, alpha = calculate_beta_alpha(stock_returns, market_returns)
        
        # CAPM Calculation
        rf = 0.0 # Assuming 0% risk-free rate
        expected_return = rf + beta * (market_returns.mean() * 252 - rf)
        
        results_data.append({
            "Stock": stock,
            "Beta": f"{beta:.2f}",
            "Expected Annual Return": f"{expected_return:.2%}",
            "Alpha (Annualized)": f"{alpha*252:.2%}"
        })
        
    results_df = pd.DataFrame(results_data)

    # --- Display Results and Charts ---
    st.subheader("CAPM Results")
    st.dataframe(results_df, use_container_width=True, hide_index=True)

    # Charts in columns
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("Stock Prices (Raw)")
        st.line_chart(close_prices[stocks_list])
    with chart_col2:
        st.subheader("Stock Prices (Normalized)")
        normalized_df = normalize_prices(close_prices[stocks_list])
        st.line_chart(normalized_df)

except Exception as e:
    st.error("An error occurred. Please select at least one stock.")
    st.error(f"Details: {e}")