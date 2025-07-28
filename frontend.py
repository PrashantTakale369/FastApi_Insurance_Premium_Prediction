import streamlit as st
import requests


API_URL = "http://localhost:8000/predict"

st.title("Insurance Primium Prediction")
st.markdown("Enter your details below to predict Insurance Primium.")


# Input fields

age = st.number_input("Age", min_value=0, max_value=120, value=30)
weight = st.number_input("Weight (in kg)", min_value=0.0, value=70.0)
height = st.number_input("Height (in cm)", min_value=0, value=170)
smoker = st.selectbox("Are you a smoker?", ["yes", "no"])       
city = st.text_input("City",value="New York")
income_lpa = st.number_input("Annual Income (in LPA)", min_value=0, value=5)
occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job']
)


if st.button("Predict Insurance Primium"):
    
    data = {

        "age": age,
        "weight": weight, 
        "height": height, 
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Insurance Primium Prediction: **{result['Predicted_Category']}**")
        else:
            st.error("API Error:{response.status_code}-{response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the API. Please ensure the API is running in 8080 port.")
