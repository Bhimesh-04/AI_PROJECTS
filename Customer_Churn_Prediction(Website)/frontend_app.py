import streamlit as st
import requests
import plotly.express as px

st.set_page_config(page_title="Churn Prediction", layout="centered")
st.title("🔍 Telco Customer Churn Prediction")

# --- INPUT SECTION ---
tenure = st.slider("Tenure (in months)", min_value=0, max_value=72, value=12)
monthly_charges = st.slider("Monthly Charges", min_value=0.0, max_value=150.0, value=70.0, step=0.1)

internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

# --- FEATURE ENCODING ---
input_data = {
    "tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "InternetService_DSL": 1 if internet_service == "DSL" else 0,
    "InternetService_Fiber_optic": 1 if internet_service == "Fiber optic" else 0,
    "OnlineSecurity_No": 1 if online_security == "No" else 0,
    "OnlineSecurity_Yes": 1 if online_security == "Yes" else 0,
    "TechSupport_No": 1 if tech_support == "No" else 0,
    "TechSupport_Yes": 1 if tech_support == "Yes" else 0,
    "Contract_One_year": 1 if contract == "One year" else 0,
    "Contract_Two_year": 1 if contract == "Two year" else 0
}

# --- PREDICTION ---
if st.button("📊 Predict Churn"):
    response = requests.post("http://127.0.0.1:8000/predict", json=input_data)

    if response.status_code == 200:
        result = response.json()
        churn_prob = result["churn_probability"]
        prediction = result["prediction"]

        st.subheader("Prediction Result")
        st.success(f"Churn Prediction: **{prediction}**")
        st.metric("Churn Probability", f"{churn_prob:.2%}")

        # --- PIE CHART ---
        fig = px.pie(
            names=["Will Churn", "Will Not Churn"],
            values=[churn_prob, 1 - churn_prob],
            title="📈 Churn Probability Distribution",
            color_discrete_sequence=["red", "green"]
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("❌ API call failed. Make sure your FastAPI backend is running.")
