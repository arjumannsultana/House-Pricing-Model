import streamlit as st
import pickle
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #f7f8fa;
    color: #1a1a2e;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 48px 32px 64px !important;
    max-width: 780px !important;
}

/* ── Page header ── */
.page-header {
    margin-bottom: 36px;
}
.page-header h1 {
    font-size: 28px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0 0 6px 0;
    letter-spacing: -0.4px;
}
.page-header p {
    font-size: 14px;
    color: #6b7280;
    margin: 0;
    font-weight: 400;
}
.header-rule {
    height: 3px;
    width: 40px;
    background: #2563eb;
    border-radius: 2px;
    margin: 12px 0 0 0;
}

/* ── Section card ── */
.section-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px 24px 18px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.section-label {
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #2563eb;
    margin-bottom: 20px;
}

/* ── Input labels ── */
.stNumberInput label,
.stSelectbox label,
.stSlider label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #374151 !important;
}

/* ── Inputs ── */
.stNumberInput input {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    font-size: 15px !important;
    color: #1a1a2e !important;
    background: #fafafa !important;
}
.stNumberInput input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
div[data-baseweb="select"] > div {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    background: #fafafa !important;
    color: #1a1a2e !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] div[role="slider"] {
    background: #2563eb !important;
    border: 2px solid #fff !important;
    box-shadow: 0 0 0 2px #2563eb !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2) {
    background: #2563eb !important;
}

/* ── Button ── */
.stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    height: 50px !important;
    width: 100% !important;
    transition: background 0.2s, transform 0.15s !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.25) !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.35) !important;
    color: #ffffff !important;
}

/* ── Result box ── */
.result-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #2563eb;
    border-radius: 12px;
    padding: 28px 32px;
    margin-top: 24px;
    animation: fadeIn 0.35s ease forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #2563eb;
    margin-bottom: 8px;
}
.result-price {
    font-size: 38px;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: -0.8px;
    margin-bottom: 6px;
}
.result-meta {
    font-size: 13px;
    color: #6b7280;
    font-weight: 400;
}
.result-chips {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 18px;
}
.chip {
    background: #fff;
    border: 1px solid #dbeafe;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #374151;
    font-weight: 500;
}

/* ── Number input steppers ── */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    border-radius: 6px !important;
    border-color: #d1d5db !important;
    color: #374151 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="page-header">
    <h1>🏠 House Price Predictor</h1>
    <p>Enter property details below to get an instant AI-based price estimate.</p>
    <div class="header-rule"></div>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return pickle.load(open("model/model.pkl", "rb"))

model = load_model()

# ---------------- SECTION 1 ----------------
st.markdown("""
<div class="section-card">
    <div class="section-label">Property Dimensions</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")
with col1:
    area      = st.number_input("Area (sqft)", 500, 10000, 1500, step=50)
    bedrooms  = st.number_input("Bedrooms", 1, 10, 3)
with col2:
    bathrooms = st.number_input("Bathrooms", 1, 10, 2)
    floors    = st.number_input("Floors", 1, 5, 1)

# ---------------- SECTION 2 ----------------
st.markdown("""
<div class="section-card">
    <div class="section-label">Additional Details</div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2, gap="medium")
with col3:
    age    = st.number_input("Age of House (Years)", 0, 100, 5)
    garage = st.selectbox("Garage Available?", ["No", "Yes"])
with col4:
    location_score = st.slider("Location Score (1–10)", 1, 10, 5,
                               help="1 = Outskirts · 10 = Prime location")

garage_value = 1 if garage == "Yes" else 0

# ---------------- PREDICT ----------------
st.write("")
predict_btn = st.button("Predict House Price")

if predict_btn:
    input_data = np.array([[area, bedrooms, bathrooms, floors, age, garage_value, location_score]])
    prediction = model.predict(input_data)
    price = prediction[0]

    if price >= 1_00_00_000:
        price_str = f"₹ {price/1_00_00_000:.2f} Cr"
    elif price >= 1_00_000:
        price_str = f"₹ {price/1_00_000:.2f} L"
    else:
        price_str = f"₹ {price:,.0f}"

    price_per_sqft = price / area

    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Estimated Price</div>
        <div class="result-price">{price_str}</div>
        <div class="result-meta">Based on your inputs · ₹ {price_per_sqft:,.0f} per sqft</div>
        <div class="result-chips">
            <span class="chip">📐 {area:,} sqft</span>
            <span class="chip">🛏 {bedrooms} Bed · {bathrooms} Bath</span>
            <span class="chip">🏢 {floors} Floor{'s' if floors > 1 else ''}</span>
            <span class="chip">📅 {age} yrs old</span>
            <span class="chip">🚗 Garage: {garage}</span>
            <span class="chip">📍 Score {location_score}/10</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()