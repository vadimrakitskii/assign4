# Import necessary packages (Make sure to also include in "requirements.txt" in this repository.)
import streamlit as st
import pandas as pd
 
# Print Title for the App
st.title("Microsoft Stock Data Dashboard by Vadim Rakitskii")
 
# Read CSV file with stock data (CSV file must be in 'main' folder for your assignment 4 repository)
df = pd.read_csv("msft.csv")
 
# Use Date as the x-axis for all charts (first 10 characters strip any time/timezone suffix)
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"].astype(str).str[:10])
    df = df.set_index("Date")
 
# Market Cap Chart data: Closing Price x Volume (in USD billions)
market_cap = df["Close"] * df["Volume"] / 1e9
 
# Set up the 4 tabs on the Dashboard
tabs = st.tabs(["📋 Raw Data", "📈 Price Chart", "📊 Volume Chart", "Market Cap Chart"])
 
# Tab 1: Raw Data
with tabs[0]:
    st.subheader("Raw Data for MSFT")
    st.dataframe(df, width="stretch")
 
# Tab 2: Closing Price Chart
with tabs[1]:
    st.subheader("Closing Price for MSFT")
    st.line_chart(df["Close"])
 
# Tab 3: Volume Chart
with tabs[2]:
    st.subheader("Volume for MSFT")
    st.bar_chart(df["Volume"])
 
# Tab 4: Market Cap Chart (Price x Volume)
with tabs[3]:
    st.subheader("Market Cap for MSFT (Price x Volume, USD billions)")
    st.line_chart(market_cap)
 
