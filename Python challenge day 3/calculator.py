import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮")

st.title("🧮 Simple Calculator")

# Number inputs
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

# Operation dropdown
operation = st.selectbox("Select Operation", ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)"])

# Calculator logic
def calculate(a, b, op):
    if op == "Add (+)":
        return a + b
    elif op == "Subtract (-)":
        return a - b
    elif op == "Multiply (×)":
        return a * b
    elif op == "Divide (÷)":
        if b == 0:
            return "Error: Cannot divide by zero"
        return a / b

# Display result instantly
result = calculate(num1, num2, operation)
st.subheader("Result:")
st.write(f"### {result}")
