# pages/utils/model_training.py
import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import datetime

def get_data(ticker):
    """Fetches stock data from the beginning of the year."""
    start_date = f"{datetime.date.today().year}-01-01"
    data = yf.download(ticker, start=start_date)
    return data[['Close']]

def check_stationarity(timeseries):
    """Checks for stationarity using the Augmented Dickey-Fuller test."""
    result = adfuller(timeseries)
    return result[1] # Return p-value

def get_differencing_order(data):
    """Finds the order of differencing 'd' required to make the series stationary."""
    d = 0
    p_value = check_stationarity(data)
    while p_value > 0.05:
        data = data.diff().dropna()
        p_value = check_stationarity(data)
        d += 1
    return d

def get_rolling_mean(data):
    """Calculates the 7-day rolling mean to smooth the data."""
    return data.rolling(window=7).mean().dropna()

def scale_data(data):
    """Scales the data using StandardScaler."""
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler

def inverse_scale_data(scaled_data, scaler):
    """Performs inverse scaling."""
    return scaler.inverse_transform(scaled_data)

def fit_model(data, d_order):
    """Fits an ARIMA model and forecasts the next 30 days."""
    # Note: ARIMA orders (p,q) are hardcoded as per the video's description.
    # In practice, these are usually found using techniques like ACF/PACF plots or auto_arima.
    p_order, q_order = 30, 30
    model = ARIMA(data, order=(p_order, d_order, q_order))
    model_fit = model.fit()
    forecast = model_fit.get_forecast(steps=30)
    return forecast.predicted_mean

def evaluate_model(data, d_order):
    """Evaluates the ARIMA model by calculating RMSE on a test set."""
    train_size = int(len(data) * 0.8)
    train, test = data[0:train_size], data[train_size:len(data)]
    
    model = ARIMA(train, order=(30, d_order, 30))
    model_fit = model.fit()
    predictions = model_fit.forecast(steps=len(test))
    
    rmse = np.sqrt(mean_squared_error(test, predictions))
    return rmse

def get_forecast(data, d_order, scaler):
    """Gets the 30-day forecast and returns it as a DataFrame."""
    prediction = fit_model(data, d_order)
    inversed_prediction = inverse_scale_data(prediction.reshape(-1, 1), scaler)
    
    start_date = pd.to_datetime(data.index[-1]) + datetime.timedelta(days=1)
    date_range = pd.date_range(start=start_date, periods=30)
    
    forecast_df = pd.DataFrame(inversed_prediction, index=date_range, columns=['Forecast'])
    return forecast_df