import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch stock data from Financial Modeling Prep API
def fetch_stock_data(symbols):
    api_key = os.getenv("API_KEY")
    base_url = "https://financialmodelingprep.com/api/v3"
    data = {}
    for symbol in symbols:
        url = f"{base_url}/quote/{symbol}?apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data[symbol] = response.json()[0]
        else:
            st.error(f"Error fetching data for {symbol}: {response.status_code}")
    return pd.DataFrame(data).T

# Fetch historical stock data for visualization
def fetch_historical_data(symbol, start_date, end_date):
    api_key = os.getenv("API_KEY")
    base_url = "https://financialmodelingprep.com/api/v3/historical-price-full"
    url = f"{base_url}/{symbol}?from={start_date}&to={end_date}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data['historical'])
    else:
        st.error(f"Error fetching historical data for {symbol}: {response.status_code}")
        return pd.DataFrame()

# Streamlit app
def main():
    st.title("Stock Data Dashboard")

    # Input fields for stock symbols and date range
    symbols = st.text_input("Enter stock symbols (comma-separated)", "GOOGL,META,MSFT,AAPL").split(",")
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2024-01-01"))

    # Fetch current stock data
    if os.getenv("API_KEY"):
        df = fetch_stock_data(symbols)
        st.subheader("Current Stock Data")
        st.write(df)

        # Fetch and display historical data
        st.subheader("Historical Stock Data")
        for symbol in symbols:
            historical_df = fetch_historical_data(symbol, start_date, end_date)
            if not historical_df.empty:
                st.write(f"Historical Data for {symbol}")
                st.line_chart(historical_df.set_index('date')['close'])
    else:
        st.error("API Key is missing")

if __name__ == "__main__":
    main()
