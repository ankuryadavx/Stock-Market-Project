Stock Market Analysis & Forecasting Dashboard
An interactive web application built with Streamlit for comprehensive stock market analysis. This tool allows users to perform in-depth technical analysis, forecast future stock prices using an ARIMA model, and evaluate investments using the Capital Asset Pricing Model (CAPM).

(Note: Replace the line above with a screenshot or a GIF of your running application.)

✨ Features
Multi-Page Interface: A clean, navigable app with separate sections for different types of analysis.

Technical Analysis:

Interactive Candlestick and Line charts.

Key technical indicators: RSI, MACD, and 50-Day Moving Average.

Dynamic time-period selection (5D, 1M, 6M, 1Y, 5Y).

Display of key company metrics, financial ratios, and historical data tables.

Time Series Forecasting:

Predicts the next 30 days of a stock's closing price.

Uses a robust ARIMA (AutoRegressive Integrated Moving Average) model.

Displays model performance (RMSE) and visualizes the forecast against historical data.

CAPM Analysis:

Calculates and compares Beta and expected returns for multiple stocks against the S&P 500 market benchmark.

Includes normalized price charts for easy comparison of stock performance over time.

🛠️ Tech Stack
Language: Python 3.11

Framework: Streamlit

Data & Analysis: Pandas, NumPy

Data Source: yfinance

Visualization: Plotly

Time Series Modeling: statsmodels, scikit-learn

Technical Indicators: pandas-ta

