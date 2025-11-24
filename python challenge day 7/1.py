import streamlit as st
import csv
import os
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "workout_log.csv"


# ---------------------------------------------------
# Initialize CSV if not found
# ---------------------------------------------------
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "exercise", "sets", "reps", "weight", "volume"])


# ---------------------------------------------------
# Add workout entry
# ---------------------------------------------------
def add_entry(exercise, sets, reps, weight):
    today = datetime.now().strftime("%Y-%m-%d")
    volume = sets * reps * weight  # total weight lifted

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, exercise, sets, reps, weight, volume])


# ---------------------------------------------------
# Load data
# ---------------------------------------------------
def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()
    return pd.read_csv(CSV_FILE)


# ---------------------------------------------------
# Calculate weekly progress
# ---------------------------------------------------
def get_weekly_data(df):
    if df.empty:
        return None

    today = datetime.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    last_7_str = [d.strftime("%Y-%m-%d") for d in last_7_days]

    weekly_df = df[df["date"].isin(last_7_str)]

    if weekly_df.empty:
        return None

    # Sum volume per day
    progress = weekly_df.groupby("date")["volume"].sum().reset_index()
    progress = progress.sort_values("date")

    return progress


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.set_page_config(page_title="Gym Workout Logger", page_icon="💪", layout="centered")
st.title("💪 Gym Workout Logger")

init_csv()

tab1, tab2, tab3 = st.tabs(["➕ Log Workout", "📅 Weekly Progress", "📜 Workout History"])


# ---------------------------------------------------
# TAB 1 — Log Workout
# ---------------------------------------------------
with tab1:
    st.subheader("Add Today's Workout")

    exercise = st.text_input("Exercise name (Bench Press, Squat, etc.)")
    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)
    weight = st.number_input("Weight (kg)", min_value=1, step=1)

    if st.button("Log Workout"):
        if exercise.strip() == "":
            st.error("Please enter an exercise name.")
        else:
            add_entry(exercise, sets, reps, weight)
            st.success(f"Logged: {exercise} ({sets} sets × {reps} reps × {weight}kg)")


# ---------------------------------------------------
# TAB 2 — Weekly Progress Graph
# ---------------------------------------------------
with tab2:
    st.subheader("📅 Weekly Progress (Total Volume)")

    df = load_data()
    weekly = get_weekly_data(df)

    if weekly is None:
        st.info("Not enough data for weekly graph.")
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(weekly["date"], weekly["volume"], marker='o', linewidth=3)
        ax.set_title("Weekly Training Volume")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Volume (sets × reps × weight)")
        plt.xticks(rotation=45)
        ax.grid(True)

        st.pyplot(fig)


# ---------------------------------------------------
# TAB 3 — Full Workout Table
# ---------------------------------------------------
with tab3:
    st.subheader("📜 All Workout Records")

    df = load_data()

    if df.empty:
        st.info("No workout history yet.")
    else:
        st.dataframe(df, use_container_width=True)
