import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import sys

def get_stock_data(ticker):
    """Fetches historical stock data."""
    try:
        stock = yf.Ticker(ticker)
        # Get all available data
        data = stock.history(period="max")
        if data.empty:
            print(f"Error: No data found for ticker '{ticker}'. It may be delisted or an invalid ticker.")
            sys.exit(1)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        sys.exit(1)

def train_model(data):
    """Trains a model on percentage returns."""
    # Calculate daily percentage return
    data['Return'] = data['Close'].pct_change()
    
    # Drop missing values
    data.dropna(inplace=True)
    
    # Features (X) and Target (y)
    # We use previous day's return to predict next day's return
    X = data['Return'].shift(1).to_frame()
    y = data['Return'].to_frame()
    
    # Drop the first row with NaN in X
    X.dropna(inplace=True)
    y = y.iloc[1:] # Align y with X
    
    if X.empty:
        print("Error: Not enough data to train the model after processing.")
        sys.exit(1)

    model = LinearRegression()
    model.fit(X, y)
    return model, X.iloc[-1].values.reshape(1, -1)

def predict_returns(model, last_return):
    """Predicts future returns."""
    # Predict the next day's return
    daily_prediction = model.predict(last_return)[0][0]
    
    # Define trading days for each period
    periods = {
        "1 Day": 1,
        "1 Week": 5,
        "1 Month": 21,
        "6 Months": 126,
        "1 Year": 252
    }
    
    predictions = {}
    for period_name, days in periods.items():
        # Compound the daily predicted return
        compounded_return = (1 + daily_prediction) ** days - 1
        predictions[period_name] = compounded_return
        
    return predictions

def main():
    """Main function to run the stock prediction."""
    if len(sys.argv) < 2:
        print("Usage: python stock_predictor.py <TICKER>")
        sys.exit(1)
        
    ticker = sys.argv[1].upper()
    
    print(f"Fetching data for {ticker}...")
    stock_data = get_stock_data(ticker)
    
    print("Training model...")
    model, last_return = train_model(stock_data)
    
    print("Making predictions...")
    predictions = predict_returns(model, last_return)
    
    print("\n--- Predicted Returns ---")
    print(f"Disclaimer: These predictions are from a simplified model and should not be used for real investment decisions.\n")
    for period, ret in predictions.items():
        print(f"{period}: {ret:.2%}")

if __name__ == "__main__":
    main()
