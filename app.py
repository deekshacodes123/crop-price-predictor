
# ============================================
# Agriculture Crop Price Prediction App
# Author: Deeksha
# ============================================

import streamlit as st
import pandas as pd
import pickle

# ─────────────────────────────────────────
# Configure application settings
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Crop Price Predictor",
    page_icon="🌾",
    layout="centered"
)

# ─────────────────────────────────────────
# Application header
# ─────────────────────────────────────────
st.title("🌾 Crop Price Predictor")
st.write("State aur Commodity choose karo")
st.divider()

# ─────────────────────────────────────────
# Collect user inputs
# ─────────────────────────────────────────
state = st.selectbox(
    "State Chuno:",
    options=sorted(df["state"].unique())
)

commodity = st.selectbox(
    "Commodity Chuno:",
    options=sorted(df["commodity"].unique())
)

# ─────────────────────────────────────────
# Generate prediction on button click
# ─────────────────────────────────────────
if st.button("🔍 Price Predict Karo"):

    # Prepare encoded input features for the prediction model
    input_data = pd.DataFrame({
        "state_encoded": [le_state.transform([state])[0]],
        "commodity_encoded": [le_commodity.transform([commodity])[0]],
        "district_encoded": [0],
        "market_encoded": [0]
    })

    # Predict the price category
    prediction = model3.predict(input_data)
    result = le_label.inverse_transform(prediction)[0]

    # Retrieve historical records for the selected inputs
    filtered = df[
        (df["state"] == state) &
        (df["commodity"] == commodity)
    ]

    # Map predicted category to a price range and visual indicator
    if result == "CHEAP":
        price_range = "₹0 - ₹1,000"
        color = "green"
        emoji = "🟢"
    elif result == "MEDIUM":
        price_range = "₹1,000 - ₹4,000"
        color = "orange"
        emoji = "🟡"
    else:
        price_range = "₹4,000+"
        color = "red"
        emoji = "🔴"

    # Display prediction results
    st.divider()
    st.subheader("📊 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Category", f"{emoji} {result}")
        st.metric("Price Range", price_range)

    with col2:
        if len(filtered) > 0:
            avg = int(filtered["modal_price"].mean())
            min_p = int(filtered["min_price"].min())
            max_p = int(filtered["max_price"].max())

            st.metric("Average Price", f"₹{avg}")
            st.metric("Min Price", f"₹{min_p}")
            st.metric("Max Price", f"₹{max_p}")
        else:
            st.warning("Historical data nahi mila!")
