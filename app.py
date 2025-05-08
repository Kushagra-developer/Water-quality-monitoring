import os
import streamlit as st
import joblib
import json

# Setup correct base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'water_quality_model.pkl')

# Load model
model = joblib.load(MODEL_PATH)

# Prediction function
def predict_water_quality(ph, tds, turbidity, temperature):
    features = [[ph, tds, turbidity, temperature]]
    prediction = model.predict(features)
    return prediction[0]

# Save data to JSON
def save_data(ph, tds, turbidity, temperature, prediction):
    data = {
        'ph': ph,
        'tds': tds,
        'turbidity': turbidity,
        'temperature': temperature,
        'prediction': prediction
    }
    json_path = os.path.join(BASE_DIR, 'data.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    else:
        existing = []

    existing.append(data)

    with open(json_path, 'w') as f:
        json.dump(existing, f, indent=4)

# -------------------------------------------
# 🚀 Streamlit App UI Starts Here
# -------------------------------------------

# Set page configuration
st.set_page_config(
    page_title="Delhi Water Quality Monitoring 🌊",
    page_icon="🌊",
    layout="centered",
)

# Custom CSS for sexy UI
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #74ebd5 0%, #ACB6E5 100%);
        font-family: 'Poppins', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(to right, #00b09b, #96c93d);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #96c93d, #00b09b);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .record-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .record-card:hover {
        background-color: #f0fdf4;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Water wave banner
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌊 Delhi Water Quality Monitoring</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Real-time prediction of water quality based on input parameters.</p>", unsafe_allow_html=True)
st.write("---")

# Input form
with st.form("water_quality_form"):
    st.subheader("🔹 Enter Water Parameters:")
    
    ph = st.number_input(
        'pH (Acidity/Alkalinity)',
        format="%.2f",
        help="Ideal range: 6.5 to 8.5"
    )
    tds = st.number_input(
        'TDS (Total Dissolved Solids, ppm)',
        format="%.2f",
        help="Ideal drinking water TDS: < 500 ppm"
    )
    turbidity = st.number_input(
        'Turbidity (NTU)',
        format="%.2f",
        help="Safe range: < 5 NTU"
    )
    temperature = st.number_input(
        'Temperature (°C)',
        format="%.2f",
        help="Normal range for water bodies: 20°C - 30°C"
    )

    submit_button = st.form_submit_button(label="🔍 Predict Water Quality")

if submit_button:
    prediction = predict_water_quality(ph, tds, turbidity, temperature)
    st.success(f"🌟 Water Quality Prediction: **{prediction}**")

    save_data(ph, tds, turbidity, temperature, prediction)
    st.info('✅ Your data has been recorded successfully!')

# Show history records
st.write("---")
st.subheader("📜 Previous Monitoring Records:")

json_path = os.path.join(BASE_DIR, 'data.json')
if os.path.exists(json_path):
    with open(json_path, 'r') as f:
        records = json.load(f)
        for rec in records:
            st.markdown(
                f"<div class='record-card'>"
                f"<b>pH:</b> {rec['ph']} | "
                f"<b>TDS:</b> {rec['tds']} ppm | "
                f"<b>Turbidity:</b> {rec['turbidity']} NTU | "
                f"<b>Temp:</b> {rec['temperature']}°C | "
                f"<b>Prediction:</b> {rec['prediction']}</div>", 
                unsafe_allow_html=True
            )
else:
    st.info("No monitoring records found yet. Start by making your first prediction!")