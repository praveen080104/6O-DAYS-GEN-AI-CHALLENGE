import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Splitter", page_icon="💸", layout="centered")

# --- Custom CSS for UI ---
st.markdown("""
<style>
    .title {
        text-align:center;
        font-size:36px !important;
        color:#4CAF50;
        font-weight:700;
        margin-bottom:10px;
    }
    .subtitle {
        text-align:center;
        font-size:18px !important;
        color:#666;
        margin-bottom:30px;
    }
    .result-box {
        padding:15px;
        border-radius:10px;
        background:#2d2d2d;
        margin-top:10px;
        border-left:5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💸 Expense Splitter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Split bills easily with your friends</div>', unsafe_allow_html=True)

# ---------------- MAIN INPUT -----------------

st.header("Enter Expense Details")

# ⬇️ NEW DROPDOWN FOR EXPENSE TYPE
expense_type = st.selectbox(
    "Type of Expense",
    ["Dinner", "Trip", "Shopping", "Rent", "Party", "Snacks", "Travel", "Tickets", "Other"]
)

total_amount = st.number_input("Total Expense Amount", min_value=0.0, step=10.0, format="%.2f")

num_people = st.number_input("Number of People", min_value=1, step=1)

st.write("### Enter Names & Contributions")

people = []
contributions = []

for i in range(int(num_people)):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Name {i+1}")
    with col2:
        amount = st.number_input(f"Paid by {name if name else 'Person '+str(i+1)}", min_value=0.0, step=10.0)
    people.append(name)
    contributions.append(amount)

# ---------------- CALCULATE SPLIT -----------------

if st.button(f"Calculate Split for {expense_type} 💰"):
    df = pd.DataFrame({
        "Name": people,
        "Paid": contributions
    })

    if df["Paid"].sum() != total_amount:
        st.error("❌ Error: Total contributions do not match the total amount.")
    else:
        st.success(f"✔ Split Calculated Successfully for **{expense_type}**!")

        equal_share = total_amount / num_people
        df["Balance"] = df["Paid"] - equal_share

        st.write("### 💵 Individual Summary")
        st.dataframe(df)

        debtors = df[df["Balance"] < 0]
        creditors = df[df["Balance"] > 0]

        st.write("### 🔄 Who Owes Whom?")

        payments = []

        for i, debtor in debtors.iterrows():
            for j, creditor in creditors.iterrows():
                if debtor["Balance"] == 0:
                    break

                amount_to_pay = min(creditor["Balance"], abs(debtor["Balance"]))

                if amount_to_pay > 0:
                    payments.append(f"**{debtor['Name']} ➝ {creditor['Name']}: ₹{amount_to_pay:.2f}**")
                    df.loc[i, "Balance"] += amount_to_pay
                    df.loc[j, "Balance"] -= amount_to_pay

        # Display results
        for p in payments:
            st.markdown(f'<div class="result-box">{p}</div>', unsafe_allow_html=True)

        if not payments:
            st.info("🎉 Everyone is settled! No payments needed.")

# Footer
st.markdown("<br><center>Built with ❤️ using Streamlit</center>", unsafe_allow_html=True)
