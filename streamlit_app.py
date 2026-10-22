# Import necessary packages (Make sure to also include in "requirements.txt" in this repository.)
import streamlit as st
import pandas as pd

# Print Title for the App
st.title("Microsoft Stock Data Dashboard by Vadim Rakitskii")

# Read CSV file with stock data (CSV file must be in 'main' folder for your assignment 4 repository) 
df = pd.read_csv("msft.csv")

# Set up the 3 tabs on the Dashboard
tabs = st.tabs(["📋 Raw Data", "📈 Price Chart", "📊 Volume Chart", "Fourth Custom Tab"])

# Tab 1: Raw Data
with tabs[0]:
    st.subheader(f"Raw Data for MSFT")
    st.dataframe(df, use_container_width=True)

# Tab 2: Closing Price Chart
with tabs[1]:
    st.subheader(f"Closing Price for MSFT")
    st.line_chart(df['Close'])

# Tab 3: Volume Chart
with tabs[2]:
    st.subheader(f"Volume for MSFT")
    st.bar_chart(df['Volume'])

# Tab 4: Volume Chart
with tabs[3]:
    st.subheader(f"Mystery Tab")
    st.title("Circle")
 
    df2 = pd.DataFrame({"x": [0], "y": [0]})
 
    st.vega_lite_chart(
        df2,
        {
            "height": 300,
            "mark": {"type": "circle", "size": 40000, "color": "steelblue", "opacity": 1},
            "encoding": {
                "x": {"field": "x", "type": "quantitative", "axis": None, "scale": {"domain": [-1, 1]}},
                "y": {"field": "y", "type": "quantitative", "axis": None, "scale": {"domain": [-1, 1]}},
            },
            "config": {"view": {"stroke": None}},
        },
    )
