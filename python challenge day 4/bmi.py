import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="BMI Calculator", page_icon="🏋️", layout="centered")

st.markdown("<h1 style='text-align:center;'>🏋️ BMI Calculator</h1>", unsafe_allow_html=True)
st.write("Enter your height and weight to calculate your BMI.")

# --- Input Section ---
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, step=0.1)

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category


# --- Output Section ---
if st.button("Calculate BMI"):
    if height > 0 and weight > 0:
        bmi, category = calculate_bmi(height, weight)
        st.success(f"Your BMI is **{bmi:.2f}**")
        st.info(f"Category: **{category}**")
    else:
        st.error("Please enter valid height and weight.")
