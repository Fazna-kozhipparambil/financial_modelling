import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Load your data
@st.cache
def load_data():
    # Example: Load data from a CSV file
    data = pd.read_csv('path/to/your/data.csv')
    return data

data = load_data()

# Title and description
st.title('Stock Market Data Visualization')
st.write('This dashboard provides visualizations of stock market data for selected companies.')

# Display raw data (optional)
if st.checkbox('Show raw data'):
    st.write(data)

# Example: Line chart of stock prices
st.subheader('Stock Price Over Time')
fig, ax = plt.subplots()
for company in ['GOOGL', 'META', 'MSFT', 'AAPL']:
    company_data = data[data['Company'] == company]
    ax.plot(company_data['Date'], company_data['Price'], label=company)
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Stock Price Over Time')
ax.legend()
st.pyplot(fig)

# Example: Interactive Plotly chart
st.subheader('Interactive Stock Price Chart')
fig = px.line(data, x='Date', y='Price', color='Company', title='Interactive Stock Price Chart')
st.plotly_chart(fig)

