# pages/2_Stock_Prediction.py
import streamlit as st
from utils import model_training as mt
from utils import plotly_figures as pf

st.set_page_config(page_title="Stock Prediction", layout="wide")
st.title("Stock Price Prediction (ARIMA Model)")

# --- User Input ---
ticker = st.text_input("Enter Stock Ticker", "TSLA")

if st.button("Predict Next 30 Days"):
    with st.spinner("Fetching data, training model, and making predictions... This may take a moment."):
        try:
            # --- Model Training and Forecasting Pipeline ---
            data = mt.get_data(ticker)
            rolling_mean_data = mt.get_rolling_mean(data)
            d_order = mt.get_differencing_order(rolling_mean_data)
            scaled_data, scaler = mt.scale_data(rolling_mean_data)
            
            # Use a DataFrame for the scaled data with the correct index
            scaled_df = pd.DataFrame(scaled_data, index=rolling_mean_data.index)
            
            rmse = mt.evaluate_model(scaled_df, d_order)
            forecast_df = mt.get_forecast(scaled_df, d_order, scaler)
            
            # --- Display Results ---
            st.subheader(f"Forecast for {ticker}")
            st.metric(label="Model RMSE (Root Mean Squared Error)", value=f"{rmse:.4f}")
            
            # Chart
            fig = pf.moving_average_forecast_chart(rolling_mean_data, forecast_df)
            st.plotly_chart(fig, use_container_width=True)
            
            # Table
            st.subheader("Forecasted Prices (Next 30 Days)")
            st.dataframe(forecast_df.style.format("{:.2f}"), use_container_width=True)
            
        except Exception as e:
            st.error(f"An error occurred during the prediction process for {ticker}.")
            st.error(f"Details: {e}")