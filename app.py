import streamlit as st
import pandas as pd
import sqlite3
import datetime

# ===============================
#   DATABASE CONNECTION
# ===============================
def get_connection():
    # Change this to MySQL or PostgreSQL if needed
    conn = sqlite3.connect("hospital.db", check_same_thread=False)
    return conn

conn = get_connection()
cursor = conn.cursor()

st.set_page_config(page_title="Healthcare Management System", layout="wide")

# ===============================
#   HELPER FUNCTIONS

def run_query(query, params=None):
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    return cursor

def fetch_df(query):
    return pd.read_sql_query(query, conn)

# ===============================
#   SIDEBAR MENU
# ===============================
st.sidebar.title("Healthcare Management System")

menu = st.sidebar.radio(
    "Choose Section:",
    [
        "Patients",
        "Doctors",
        "Appointments",
        "Prescriptions",
        "Medical Tests",
        "Patient Tests",
        "Insurance Claims"
    ]
)

# ===============================
#   PATIENTS CRUD
# ===============================
if menu == "Patients":
    st.header("👨‍⚕️ Manage Patients")

    tab1, tab2, tab3 = st.tabs(["Add Patient", "View Patients", "Delete Patient"])

    with tab1:
        st.subheader("Add New Patient")
        pid = st.number_input("Patient ID", step=1)
        name = st.text_input("Full Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        dob = st.date_input("Date of Birth")
        phone = st.text_input("Contact Number")
        reg_date = st.date_input("Registration Date")

        if st.button("Add Patient"):
            run_query("""
                INSERT INTO Patients VALUES (?, ?, ?, ?, ?, ?)
            """, (pid, name, gender, dob, phone, reg_date))
            st.success("Patient added successfully!")

    with tab2:
        st.subheader("All Patients")
        df = fetch_df("SELECT * FROM Patients")
        st.dataframe(df)

    with tab3:
        st.subheader("Delete Patient")
        del_id = st.number_input("Patient ID to delete", step=1)
        if st.button("Delete"):
            run_query("DELETE FROM Patients WHERE patient_id=?", (del_id,))
            st.success("Patient deleted.")

# ===============================
#   DOCTORS CRUD
# ===============================
if menu == "Doctors":
    st.header("🩺 Manage Doctors")

    tab1, tab2 = st.tabs(["Add Doctor", "View Doctors"])

    with tab1:
        did = st.number_input("Doctor ID", step=1)
        name = st.text_input("Full Name")
        specialty = st.text_input("Specialty")
        join = st.date_input("Joining Date")

        if st.button("Add Doctor"):
            run_query("""
                INSERT INTO Doctors VALUES (?, ?, ?, ?)
            """, (did, name, specialty, join))
            st.success("Doctor added.")

    with tab2:
        st.dataframe(fetch_df("SELECT * FROM Doctors"))

# ===============================
#   APPOINTMENTS CRUD
# ===============================
if menu == "Appointments":
    st.header("📅 Manage Appointments")

    tab1, tab2 = st.tabs(["Add Appointment", "View Appointments"])

    with tab1:
        appt_id = st.number_input("Appointment ID", step=1)
        patient_id = st.number_input("Patient ID", step=1)
        doctor_id = st.number_input("Doctor ID", step=1)
        appt_date_date = st.date_input("Appointment Date")
        appt_date_time = st.time_input("Appointment Time")
        appt_date = datetime.datetime.combine(appt_date_date, appt_date_time)
        status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])

        if st.button("Add Appointment"):
            run_query("""
                INSERT INTO Appointments VALUES (?, ?, ?, ?, ?)
            """, (appt_id, patient_id, doctor_id, appt_date, status))
            st.success("Appointment added.")

    with tab2:
        st.dataframe(fetch_df("""
            SELECT a.appointment_id, p.full_name AS patient, d.full_name AS doctor,
                   a.appointment_date, a.status
            FROM Appointments a
            LEFT JOIN Patients p ON a.patient_id = p.patient_id
            LEFT JOIN Doctors d ON a.doctor_id = d.doctor_id
        """))

# ===============================
#   PRESCRIPTIONS CRUD
# ===============================
if menu == "Prescriptions":
    st.header("💊 Manage Prescriptions")

    tab1, tab2 = st.tabs(["Add Prescription", "View Prescriptions"])

    with tab1:
        pid = st.number_input("Prescription ID", step=1)
        apptid = st.number_input("Appointment ID", step=1)
        med = st.text_input("Medicine Name")
        dose = st.text_input("Dosage")
        duration = st.number_input("Duration (days)", step=1)

        if st.button("Add Prescription"):
            run_query("""
                INSERT INTO Prescriptions VALUES (?, ?, ?, ?, ?)
            """, (pid, apptid, med, dose, duration))
            st.success("Prescription added.")

    with tab2:
        st.dataframe(fetch_df("""
            SELECT * FROM Prescriptions
        """))

# ===============================
#   MEDICAL TESTS CRUD
# ===============================
if menu == "Medical Tests":
    st.header("🧪 Manage Medical Tests")

    tab1, tab2 = st.tabs(["Add Medical Test", "View Tests"])

    with tab1:
        tid = st.number_input("Test ID", step=1)
        name = st.text_input("Test Name")
        cost = st.number_input("Cost", step=1.0)

        if st.button("Add Test"):
            run_query("""
                INSERT INTO MedicalTests VALUES (?, ?, ?)
            """, (tid, name, cost))
            st.success("Test added.")

    with tab2:
        st.dataframe(fetch_df("SELECT * FROM MedicalTests"))

# ===============================
#   PATIENT TESTS CRUD
# ===============================
if menu == "Patient Tests":
    st.header("🔬 Manage Patient Tests")

    tab1, tab2 = st.tabs(["Add Patient Test", "View Patient Tests"])

    with tab1:
        ptid = st.number_input("Patient Test ID", step=1)
        pid = st.number_input("Patient ID", step=1)
        tid = st.number_input("Test ID", step=1)
        tdate = st.date_input("Test Date")
        result = st.text_area("Result")

        if st.button("Add Patient Test"):
            run_query("""
                INSERT INTO PatientTests VALUES (?, ?, ?, ?, ?)
            """, (ptid, pid, tid, tdate, result))
            st.success("Patient test added.")

    with tab2:
        st.dataframe(fetch_df("""
            SELECT pt.patient_test_id, p.full_name AS patient,
                   t.test_name AS test, pt.test_date, pt.result
            FROM PatientTests pt
            LEFT JOIN Patients p ON pt.patient_id = p.patient_id
            LEFT JOIN MedicalTests t ON pt.test_id = t.test_id
        """))

# ===============================
#   INSURANCE CLAIMS CRUD
# ===============================
if menu == "Insurance Claims":
    st.header("📄 Manage Insurance Claims")

    tab1, tab2 = st.tabs(["Add Claim", "View Claims"])

    with tab1:
        cid = st.number_input("Claim ID", step=1)
        pid = st.number_input("Patient ID", step=1)
        amount = st.number_input("Claim Amount", step=1.0)
        cdate = st.date_input("Claim Date")
        status = st.selectbox("Status", ["Approved", "Pending", "Rejected"])

        if st.button("Add Claim"):
            run_query("""
                INSERT INTO InsuranceClaims VALUES (?, ?, ?, ?, ?)
            """, (cid, pid, amount, cdate, status))
            st.success("Claim added.")

    with tab2:
        st.dataframe(fetch_df("""
            SELECT c.claim_id, p.full_name AS patient,
                   c.claim_amount, c.claim_date, c.status
            FROM InsuranceClaims c
            LEFT JOIN Patients p ON c.patient_id = p.patient_id
        """))

