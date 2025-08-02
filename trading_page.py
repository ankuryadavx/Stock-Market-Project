# trading_page.py
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Trading App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

st.title(":chart_with_upwards_trend: Trading App")
st.header("The greatest platform for you to analyze stocks before investing.")

# You can add an image here if you have one in the same folder
# from PIL import Image
# img = Image.open("your_image_name.png")
# st.image(img, use_column_width=True)

st.markdown("""
### We provide the following services:
- **:mag: Stock Analysis:** In-depth technical analysis using interactive charts, key metrics, and historical data.
- **:crystal_ball: Stock Prediction:** Future stock price forecasting for the next 30 days using a Time Series ARIMA Model.
- **:scales: CAPM Analysis:** Compare stocks and calculate their Beta and expected returns using the Capital Asset Pricing Model.
---
**Select a service from the sidebar to get started!**
""")