import streamlit as st
import requests

# ---------------------------
# Live currency rate function
# ---------------------------
def get_usd_inr_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url).json()
        return response["rates"]["INR"]
    except:
        return 83.0  # fallback rate


# ---------------------------
# Conversion functions
# ---------------------------

def inr_to_usd(a, r): return a / r
def usd_to_inr(a, r): return a * r

def c_to_f(c): return (c * 9/5) + 32
def f_to_c(f): return (f - 32) * 5/9

def cm_to_inch(cm): return cm / 2.54
def inch_to_cm(inch): return inch * 2.54

def kg_to_lb(kg): return kg * 2.20462
def lb_to_kg(lb): return lb / 2.20462


# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Unit Converter", layout="centered")

st.title("🔄 Unit Converter")
st.write("Real-time conversion tool (INR/USD, Temp, Length, Weight)")

option = st.selectbox(
    "Choose a conversion",
    [
        "INR → USD", "USD → INR",
        "°C → °F", "°F → °C",
        "cm → inch", "inch → cm",
        "kg → lb", "lb → kg"
    ]
)

rate = get_usd_inr_rate()

if "INR" in option or "USD" in option:
    st.info(f"💱 Live USD → INR rate: **{rate}**")


value = st.number_input("Enter value:", step=0.01, format="%.2f")

if option == "INR → USD":
    result = inr_to_usd(value, rate)
    st.success(f"USD: {round(result, 4)}")

elif option == "USD → INR":
    result = usd_to_inr(value, rate)
    st.success(f"INR: {round(result, 4)}")

elif option == "°C → °F":
    st.success(f"°F: {round(c_to_f(value), 4)}")

elif option == "°F → °C":
    st.success(f"°C: {round(f_to_c(value), 4)}")

elif option == "cm → inch":
    st.success(f"Inches: {round(cm_to_inch(value), 4)}")

elif option == "inch → cm":
    st.success(f"cm: {round(inch_to_cm(value), 4)}")

elif option == "kg → lb":
    st.success(f"lb: {round(kg_to_lb(value), 4)}")

elif option == "lb → kg":
    st.success(f"kg: {round(lb_to_kg(value), 4)}")
