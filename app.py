import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Student Performance Predictor", layout="centered", page_icon="🎓")
st.title("🎓 Student Performance Predictor")
st.caption("FOAI - Final Year Project | AIML Department")
st.divider()

# --- INPUT SECTION ---
st.subheader("Enter Student Details")

student_name = st.text_input("👤 Student Full Name (Manual Entry)", placeholder="e.g. Aditya Patil")

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
if st.button("🔍 Predict Performance", use_container_width=True, type="primary"):
    if student_name.strip() == "":
        st.error("⚠️ Please enter Student Name first!")
        st.stop()

    # --- FIXED LOGIC - Normalized to 100 ---
    internal_pct = (internal / 40) * 100
    study_pct = (study_hours / 12) * 100
    assign_pct = (assignments / 10) * 100
    part_pct = (participation / 10) * 100

    # Weighted score out of 100
    total_score = (attendance * 0.25) + (prev_sem * 0.25) + (internal_pct * 0.20) + (study_pct * 0.10) + (assign_pct * 0.10) + (part_pct * 0.10)
    
    total_score = round(total_score, 1)

    if total_score >= 80:
        result = "Excellent 🌟"
    elif total_score >= 65:
        result = "Good 👍"
    elif total_score >= 50:
        result = "Average 📊"
    else:
        result = "Needs Improvement ⚠️"

    st.divider()
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(label=f"Result for {student_name}", value=result)
    with col_res2:
        st.metric(label="Total Score", value=f"{total_score}/100")
    
    st.progress(int(total_score))
    
    if total_score >= 80:
        st.success("Keep it up! Top performer.")
    elif total_score >= 50:
        st.warning("Good, but can improve with more study hours.")
    else:
        st.error("Needs attention - Low attendance / study hours.")

    # --- SAVE TO CSV ---
    new_record = {
        "Name": student_name.strip(),
        "Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Attendance": attendance,
        "Internal": internal,
        "Study Hours": study_hours,
        "Prev Sem %": prev_sem,
        "Assignments": assignments,
        "Participation": participation,
        "Performance": result,
        "Score": total_score
    }

    df_new = pd.DataFrame([new_record])
    if os.path.exists("student_records.csv"):
        df_old = pd.read_csv("student_records.csv")
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new
    df_final.to_csv("student_records.csv", index=False)
    st.toast(f"✅ Record saved for {student_name}")

# --- SHOW ALL RECORDS ---
st.divider()
st.subheader("📋 All Student Records")

if os.path.exists("student_records.csv"):
    df = pd.read_csv("student_records.csv")
    st.dataframe(df[::-1], use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button("📥 Download CSV", csv, "student_records.csv", "text/csv", use_container_width=True)
    with col_d2:
        if st.button("🗑️ Clear All Records", use_container_width=True):
            os.remove("student_records.csv")
            st.rerun()
else:
    st.info("No records yet. Add first student above.")
