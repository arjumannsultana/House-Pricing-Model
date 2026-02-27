import streamlit as st
import pickle
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #2E86C1;
    }
    .subtext {
        font-size:18px;
        color:gray;
    }
    .stButton>button {
        background-color: #2E86C1;
        color: white;
        font-size:18px;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1B4F72;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<p class="title">🏠 Smart House Price Prediction App</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Enter house details and get instant AI-based prediction</p>', unsafe_allow_html=True)

st.write("")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model/model.pkl", "rb"))

# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Enter Property Details")

    area = st.number_input("Area (sqft)", 500, 10000, 1500)
    bedrooms = st.number_input("Bedrooms", 1, 10, 3)
    bathrooms = st.number_input("Bathrooms", 1, 10, 2)
    floors = st.number_input("Floors", 1, 5, 1)

with col2:
    st.subheader("🏘 Additional Features")

    age = st.number_input("Age of House (Years)", 0, 100, 5)
    garage = st.selectbox("Garage Available?", ["No", "Yes"])
    location_score = st.slider("Location Score (1-10)", 1, 10, 5)

# Convert Garage to numeric
garage_value = 1 if garage == "Yes" else 0

st.write("")
st.write("")

# ---------------- PREDICTION BUTTON ----------------
if st.button("🚀 Predict House Price"):

    input_data = np.array([[area, bedrooms, bathrooms, floors, age, garage_value, location_score]])
    prediction = model.predict(input_data)

    st.markdown("---")
    st.success(f"💰 Estimated House Price: ₹ {prediction[0]:,.2f}")
    st.balloons()