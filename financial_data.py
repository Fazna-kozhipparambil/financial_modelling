import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fetch stock data
def fetch_stock_data(api_key, symbols):
    base_url = "https://financialmodelingprep.com/api/v3"
    data = {}
    for symbol in symbols:
        url = f"{base_url}/quote/{symbol}?apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data[symbol] = response.json()[0]
        else:
            print(f"Error fetching data for {symbol}: {response.status_code}")
    return pd.DataFrame(data).T

# Streamlit app
def main():
    st.title("Stock Data Dashboard")
    
    api_key = st.text_input("Enter your Financial Modeling Prep API Key", "")
    symbols = st.text_input("Enter stock symbols (comma-separated)", "GOOGL,META,MSFT,AAPL").split(",")
    
    if api_key:
        df = fetch_stock_data(api_key, symbols)
        st.write("Stock Data:", df)
        
        # Display charts
        if not df.empty:
            st.subheader("Stock Price Chart")
            for symbol in symbols:
                if symbol in df.index:
                    st.line_chart(df.loc[symbol, ['price']])
    else:
        st.error("API Key is required to fetch data")

if __name__ == "__main__":
    main()

