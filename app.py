import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Student Performance Predictor", layout="centered")
st.title("🎓 Student Performance Predictor")
st.caption("FOAI - Final Year Project")
st.divider()

# --- INPUT SECTION ---
st.subheader("Enter Student Details")

student_name = st.text_input("👤 Student Full Name", placeholder="e.g. Aditya Patil")

col1, col2 = st.columns(2)
with col1:
    attendance = st.slider("Attendance %", 0, 100, 75)
    internal = st.slider("Internal Marks (out of 40)", 0, 40, 28)
    study_hours = st.slider("Daily Study Hours", 0, 12, 4)

with col2:
    prev_sem = st.slider("Previous Semester %", 0, 100, 65)
    assignments = st.slider("Assignments Submitted (out of 10)", 0, 10, 8)
    participation = st.slider("Class Participation (1-10)", 1, 10, 6)

# --- PREDICT BUTTON ---
if st.button("🔍 Predict Performance", use_container_width=True):
    if student_name.strip() == "":
        st.error("⚠️ Please enter Student Name first!")
        st.stop()

    # --- Simple Prediction Logic (replace with model if you have) ---
    total_score = (attendance * 0.3) + (prev_sem * 0.3) + (internal * 1.5) + (study_hours * 4) + (assignments * 2) + (participation * 2)
    
    if total_score >= 85:
        result = "Excellent 🌟"
        color = "green"
    elif total_score >= 65:
        result = "Good 👍"
        color = "blue"
    elif total_score >= 45:
        result = "Average 📊"
        color = "orange"
    else:
        result = "Needs Improvement ⚠️"
        color = "red"

    st.divider()
    st.metric(label=f"Result for {student_name}", value=result)
    st.progress(min(int(total_score), 100))

    # --- SAVE TO CSV WITH NAME ---
    new_record = {
        "Name": student_name,
        "Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Attendance": attendance,
        "Internal": internal,
        "Study Hours": study_hours,
        "Prev Sem %": prev_sem,
        "Assignments": assignments,
        "Participation": participation,
        "Performance": result,
        "Score": int(total_score)
    }

    df_new = pd.DataFrame([new_record])

    if os.path.exists("student_records.csv"):
        df_old = pd.read_csv("student_records.csv")
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_csv("student_records.csv", index=False)
    st.success(f"✅ Record saved for {student_name}")

# --- SHOW ALL RECORDS ---
st.divider()
st.subheader("📋 All Student Records")

if os.path.exists("student_records.csv"):
    df = pd.read_csv("student_records.csv")
    st.dataframe(df[::-1], use_container_width=True) # latest first
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download All Records CSV", csv, "student_records.csv", "text/csv")
    
    if st.button("🗑️ Clear All Records"):
        os.remove("student_records.csv")
        st.rerun()
else:
    st.info("No records yet. Predict first student to see table.")
