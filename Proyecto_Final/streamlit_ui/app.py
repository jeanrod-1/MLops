import streamlit as st
import requests

st.title("Predicción de valor de casas")
data = {
    'longitude': st.number_input('Longitud'),
    'latitude': st.number_input('Latitud'),
    'housing_median_age': st.number_input('Edad media de la vivienda'),
    'total_rooms': st.number_input('Habitaciones totales'),
    'total_bedrooms': st.number_input('Dormitorios totales'),
    'population': st.number_input('Población'),
    'households': st.number_input('Hogares'),
    'median_income': st.number_input('Ingreso medio'),
    # Añadir dummies de ocean_proximity si aplica
}

if st.button("Predecir"):
    res = requests.post("http://fastapi:8000/predict", json=data)
    st.write("Predicción:", res.json())