import streamlit as st
import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

CSV_FILE = "water_log.csv"

# -----------------------------
# Initialize CSV file
# -----------------------------
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "water_ml"])


# -----------------------------
# Add water intake
# -----------------------------
def log_water(ml):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, ml])


# -----------------------------
# Read all data
# -----------------------------
def read_data():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


# -----------------------------
# Get last 7 days hydration
# -----------------------------
def get_weekly_data():
    data = read_data()
    today = datetime.now().date()

    # Initialize chart dictionary
    week = {}
    for i in range(7):
        day = today - timedelta(days=i)
        week[day.strftime("%Y-%m-%d")] = 0

    # Fill values
    for row in data:
        if row["date"] in week:
            week[row["date"]] += int(row["water_ml"])

    return dict(sorted(week.items()))


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Water Intake Tracker", page_icon="💧")

initialize_csv()

st.title("💧 Water Intake Tracker (Streamlit App)")

tab1, tab2, tab3 = st.tabs(["➕ Log Intake", "📅 Weekly Chart", "📜 History"])


# -----------------------------
# TAB 1 – LOG WATER
# -----------------------------
with tab1:
    st.subheader("Add today's water intake (ml)")

    ml = st.number_input("Enter water (ml):", min_value=1, step=50)

    if st.button("Log Water"):
        log_water(ml)
        st.success(f"Logged {ml} ml successfully!")


# -----------------------------
# TAB 2 – WEEKLY CHART
# -----------------------------
with tab2:
    st.subheader("📅 Weekly Hydration Chart (Past 7 Days)")

    week_data = get_weekly_data()
    dates = list(week_data.keys())
    values = list(week_data.values())

    # Plot chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, values, marker='o', linewidth=3)
    ax.set_title("Weekly Hydration (ml)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Water Intake (ml)")
    ax.grid(True)
    plt.xticks(rotation=45)

    st.pyplot(fig)


# -----------------------------
# TAB 3 – FULL HISTORY
# -----------------------------
with tab3:
    st.subheader("📜 Complete History")

    data = read_data()

    if data:
        st.table(data)
    else:
        st.info("No data logged yet.")
