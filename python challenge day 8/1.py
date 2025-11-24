import streamlit as st

# -------------------------------
# Static Conversion Rates (Base: INR)
# -------------------------------
rates = {
    "INR": 1,
    "USD": 0.012,   # 1 INR = 0.012 USD
    "EUR": 0.011,   # 1 INR = 0.011 EUR
    "GBP": 0.0095,  # 1 INR = 0.0095 GBP
}

# Title
st.set_page_config(page_title="Currency Converter", page_icon="💱")
st.title("💱 Currency Converter")

st.write("Convert between INR, USD, EUR, GBP using static exchange rates.")

# Inputs
col1, col2, col3 = st.columns(3)

with col1:
    from_curr = st.selectbox("From Currency", rates.keys())

with col2:
    to_curr = st.selectbox("To Currency", rates.keys())

with col3:
    amount = st.number_input("Amount", min_value=0.0, step=1.0)

# Conversion Logic
def convert(amount, from_c, to_c):
    if from_c == to_c:
        return amount
    # convert from -> INR -> target
    return amount * (1 / rates[from_c]) * rates[to_c]

result = convert(amount, from_curr, to_curr)

st.subheader("Converted Amount")
st.success(f"{amount} {from_curr} = {round(result, 2)} {to_curr}")
