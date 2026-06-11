
# ============================================
# Agriculture Crop Price Prediction App
# Author: Deeksha
# ============================================

import streamlit as st
import pandas as pd
import pickle

# ─────────────────────────────────────────
# Page Setup
# ─────────────────────────────────────────
st.set_page_config(
    page_title = "Crop Price Predictor",
    page_icon  = "🌾",
    layout     = "centered"
)

# ─────────────────────────────────────────
# Load Data and Models
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("agriculture_clean.csv")

@st.cache_resource
def load_models():
    model      = pickle.load(open("model.pkl","rb"))
    le_state   = pickle.load(open("le_state.pkl","rb"))
    le_comm    = pickle.load(open("le_commodity.pkl","rb"))
    le_dist    = pickle.load(open("le_district.pkl","rb"))
    le_market  = pickle.load(open("le_market.pkl","rb"))
    le_label   = pickle.load(open("le_label.pkl","rb"))
    return model, le_state, le_comm, le_dist, le_market, le_label

# Load karo
df = load_data()
model, le_state, le_comm, le_dist, le_market, le_label = load_models()

# ─────────────────────────────────────────
# Title
# ─────────────────────────────────────────
st.title("🌾 Crop Price Predictor")
st.write("State aur Commodity choose karo")
st.divider()

# ─────────────────────────────────────────
# User Input
# ─────────────────────────────────────────
state = st.selectbox(
    "State Chuno:",
    options = sorted(df["state"].unique())
)

commodity = st.selectbox(
    "Commodity Chuno:",
    options = sorted(df["commodity"].unique())
)

# ─────────────────────────────────────────
# Predict Button
# ─────────────────────────────────────────
if st.button("🔍 Price Predict Karo"):

    # Input DataFrame banao
    input_data = pd.DataFrame({
        "state_encoded"    : [le_state.transform([state])[0]],
        "commodity_encoded": [le_comm.transform([commodity])[0]],
        "district_encoded" : [0],
        "market_encoded"   : [0]
    })

    # Predict karo
    prediction = model.predict(input_data)
    result = le_label.inverse_transform(prediction)[0]

    # Historical data nikalo
    filtered = df[
        (df["state"] == state) &
        (df["commodity"] == commodity)
    ]

    # Price range set karo
    if result == "CHEAP":
        price_range = "Rs.0 - Rs.1,000"
        emoji = "🟢"
    elif result == "MEDIUM":
        price_range = "Rs.1,000 - Rs.4,000"
        emoji = "🟡"
    else:
        price_range = "Rs.4,000+"
        emoji = "🔴"

    # Result dikhao
    st.divider()
    st.subheader("📊 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Category", f"{emoji} {result}")
        st.metric("Price Range", price_range)

    with col2:
        if len(filtered) > 0:
            avg   = int(filtered["modal_price"].mean())
            min_p = int(filtered["min_price"].min())
            max_p = int(filtered["max_price"].max())
            st.metric("Average Price", f"Rs.{avg}")
            st.metric("Min Price", f"Rs.{min_p}")
            st.metric("Max Price", f"Rs.{max_p}")
        else:
            st.warning("Historical data nahi mila!")
