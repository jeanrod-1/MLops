import streamlit as st, requests, json, os

API_URL = os.getenv("API_URL", "http://172.30.173.0:30012")

st.title("Predicción de re-ingreso (<30d)")

with st.form("data"):
    num_lab = st.slider("Num lab procedures",1,132,40)
    meds    = st.slider("Num medications",1,81,10)
    days    = st.slider("Time in hospital (days)",1,14,3)
    # race    = st.selectbox("Race",["Caucasian","African American","Asian","Hispanic","Other"])
    submitted = st.form_submit_button("Predecir")

if submitted:
    payload = {
        "num_lab_procedures": num_lab,
        "num_medications": meds,
        "time_in_hospital": days,
        # "race": race
    }
    resp = requests.post(f"{API_URL}/predict", json=payload).json()
    st.write(resp)