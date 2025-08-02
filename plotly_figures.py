# pages/utils/plotly_figures.py

import plotly.graph_objects as go
import pandas_ta as ta
import pandas as pd
from datetime import timedelta

def plotly_table(df):
    """Creates a styled Plotly table from a DataFrame."""
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='#0D1F33',
                    align='left',
                    font=dict(color='white', size=14)),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='#F0F2F6',
                   align='left',
                   font=dict(color='#0D1F33', size=12)))
    ])
    fig.update_layout(height=450, margin=dict(l=10, r=10, t=20, b=20))
    return fig

def filter_data(df, num_period):
    """Filters DataFrame based on a time period string (e.g., '5d', '1m')."""
    if num_period[-1] == 'd':
        delta = timedelta(days=int(num_period[:-1]))
    elif num_period[-1] == 'm':
        delta = timedelta(days=int(num_period[:-1]) * 30)
    elif num_period[-1] == 'y':
        delta = timedelta(days=int(num_period[:-1]) * 365)
    else:
        return df # Return full dataframe if no valid period
    
    start_date = df['Date'].max() - delta
    return df[df['Date'] >= start_date]

def candlestick_chart(df, num_period=None):
    """Creates a Candlestick chart."""
    if num_period:
        df = filter_data(df, num_period)
        
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'])])
    fig.update_layout(title="Candlestick Chart", xaxis_rangeslider_visible=False)
    return fig

def rsi_chart(df, num_period=None):
    """Creates a Candlestick chart with an RSI subplot."""
    if num_period:
        df = filter_data(df, num_period)
        
    # NEW: Check for sufficient data for RSI (length=14)
    if len(df) < 14:
        fig = candlestick_chart(df)
        fig.update_layout(title="Candlestick Chart (Not enough data for RSI - 14 days needed)")
        return fig
        
    df.ta.rsi(close='Close', length=14, append=True)
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Candlestick'))
    
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI_14'], mode='lines', name='RSI', yaxis='y2'))
    fig.add_hline(y=70, line_dash="dash", line_color="red", yaxis="y2")
    fig.add_hline(y=30, line_dash="dash", line_color="green", yaxis="y2")

    fig.update_layout(
        title="Candlestick with RSI",
        yaxis=dict(domain=[0.3, 1]),
        yaxis2=dict(domain=[0, 0.2], title="RSI"),
        xaxis_rangeslider_visible=False
    )
    return fig
    
def macd_chart(df, num_period=None):
    """Creates a Candlestick chart with a MACD subplot."""
    if num_period:
        df = filter_data(df, num_period)

    # NEW: Check for sufficient data for MACD (slow period = 26)
    if len(df) < 26:
        fig = candlestick_chart(df)
        fig.update_layout(title="Candlestick Chart (Not enough data for MACD - 26 days needed)")
        return fig

    df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Candlestick'))
    
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD_12_26_9'], mode='lines', name='MACD', yaxis='y2'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MACDs_12_26_9'], mode='lines', name='Signal', yaxis='y2'))
    fig.add_trace(go.Bar(x=df['Date'], y=df['MACDh_12_26_9'], name='Histogram', yaxis='y2'))

    fig.update_layout(
        title="Candlestick with MACD",
        yaxis=dict(domain=[0.3, 1]),
        yaxis2=dict(domain=[0, 0.2], title="MACD"),
        xaxis_rangeslider_visible=False
    )
    return fig

def moving_average_chart(df, num_period=None):
    """Creates a Line chart with a 50-day Moving Average."""
    if num_period:
        df = filter_data(df, num_period)
    
    # NEW: Check for sufficient data for Moving Average (window=50)
    if len(df) < 50:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
        fig.update_layout(title="Close Price (Not enough data for MA50 - 50 days needed)")
        return fig
        
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], mode='lines', name='50-Day Moving Average'))
    
    fig.update_layout(title="Close Price with Moving Average")
    return fig

def moving_average_forecast_chart(df, forecast_df):
    """Creates a chart showing historical rolling average and forecasted data."""
    fig = go.Figure()
    
    # Historical Rolling Mean Price
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Rolling_Mean_Price'], 
        mode='lines', 
        name='Historical Rolling Mean Price'
    ))
    
    # Forecasted Price
    fig.add_trace(go.Scatter(
        x=forecast_df.index, 
        y=forecast_df['Forecast'], 
        mode='lines', 
        name='Future Forecasted Price',
        line=dict(dash='dash')
    ))
    
    fig.update_layout(title="Stock Price Forecast: Historical vs. Future",
                      xaxis_title="Date",
                      yaxis_title="Price")
    return fig