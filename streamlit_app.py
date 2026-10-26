# Import necessary packages (Make sure to also include in "requirements.txt" in this repository.)
import streamlit as st
import pandas as pd
import math
import time

# Print Title for the App
st.title("Microsoft Stock Data Dashboard by Vadim Rakitskii")

# Read CSV file with stock data (CSV file must be in 'main' folder for your assignment 4 repository) 
df = pd.read_csv("msft.csv")

# Set up the 3 tabs on the Dashboard
tabs = st.tabs(["📋 Raw Data", "📈 Price Chart", "📊 Volume Chart", "Surprise Tab"])

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
    st.subheader(f"Surprise Tab")
    R1, R2, K2 = 1.0, 2.0, 5.0  # tube radius, ring radius, camera distance
 
# Surface grid: theta goes around the tube, phi goes around the ring
grid = pd.DataFrame(
    [(t * 2 * math.pi / 32, p * 2 * math.pi / 96) for t in range(32) for p in range(96)],
    columns=["theta", "phi"],
)
cos_t, sin_t = grid["theta"].map(math.cos), grid["theta"].map(math.sin)
cos_p, sin_p = grid["phi"].map(math.cos), grid["phi"].map(math.sin)
cx = R2 + R1 * cos_t
cy = R1 * sin_t
 
SPEC = {
    "width": 420,
    "height": 420,
    "mark": {"type": "circle", "opacity": 1},
    "encoding": {
        "x": {"field": "x", "type": "quantitative", "axis": None, "scale": {"domain": [-4, 4]}},
        "y": {"field": "y", "type": "quantitative", "axis": None, "scale": {"domain": [-4, 4]}},
        "size": {"field": "size", "type": "quantitative", "scale": None},  # nearer = bigger
        "color": {
            "field": "light",
            "type": "quantitative",
            "legend": None,
            "scale": {"domain": [-1.4, 1.4], "range": ["#2b1608", "#c47a3a", "#ffe3b8"]},
        },
    },
    "config": {"view": {"stroke": None}},
    "usermeta": {"embedOptions": {"renderer": "canvas"}},  # canvas redraws faster than SVG
}
 
 
def donut(A, B):
    """Rotate the torus by angles A (x-axis) and B (z-axis), project it, and shade it."""
    cA, sA, cB, sB = math.cos(A), math.sin(A), math.cos(B), math.sin(B)
    x = cx * (cB * cos_p + sA * sB * sin_p) - cy * cA * sB
    y = cx * (sB * cos_p - sA * cB * sin_p) + cy * cA * cB
    z = K2 + cA * cx * sin_p + cy * sA
    light = (cos_p * cos_t * sB - cA * cos_t * sin_p - sA * sin_t
             + cB * (cA * sin_t - cos_t * sA * sin_p))
    df = pd.DataFrame({"x": K2 * x / z, "y": K2 * y / z, "z": z, "light": light, "size": 200 * (K2 / z) ** 2})
    return df.sort_values("z", ascending=False).drop(columns="z").round(3)  # far points first
 
 
# Invisible point (size 0). Streamlit only redraws chart data when the row count changes,
# so every other frame gets this extra row to force a redraw.
PAD = pd.DataFrame({"x": [0.0], "y": [0.0], "light": [0.0], "size": [0.0]})
 
 
# Streamlit reruns this fragment on a timer, so there is no blocking loop or time.sleep.
# The angle comes from the clock, so the spin speed stays the same even if frames drop.
@st.fragment(run_every=0.05)
def spin():
    st.session_state.frame = st.session_state.get("frame", 0) + 1
    t = time.time()
    df = donut(2.0 * t, 1.0 * t)
    if st.session_state.frame % 2:
        df = pd.concat([df, PAD])
    st.vega_lite_chart(df, SPEC, width="content")
 
 
spin()
