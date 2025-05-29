import streamlit as st
import requests
import os
import base64

API_URL = os.getenv("API_URL", "http://172.30.173.0:30012")

st.title("Predicción de Precio de Casa")

with st.form("house_form"):
    bed = st.slider("Número de habitaciones", 1, 10, 3)
    bath = st.slider("Número de baños", 1, 10, 2)
    acre_lot = st.number_input("Tamaño del lote (acres)", min_value=0.0, value=0.5, step=0.1)
    house_size = st.number_input("Tamaño de la casa (pies cuadrados)", min_value=100, value=2000, step=100)
    submitted = st.form_submit_button("Predecir")

if submitted:
    payload = {
        "bed": bed,
        "bath": bath,
        "acre_lot": acre_lot,
        "house_size": house_size
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        response.raise_for_status()
        result = response.json()
        st.success(f"Precio estimado: ${result['predicted_price']:,.2f}")
    except Exception as e:
        st.error(f"Error en la predicción: {e}")

st.markdown("---")
st.header("Modelo en Producción")

try:
    response = requests.get(f"{API_URL}/current-model")
    response.raise_for_status()
    model_info = response.json()
    st.info(f"🔧 Modelo actual en producción: **{model_info['model_name']}**, versión **{model_info['version']}**, run ID: `{model_info['run_id']}`")
except Exception as e:
    st.error(f"No se pudo obtener el modelo actual: {e}")

st.markdown("---")
st.header("Historial de modelos (MLflow)")

if st.button("Cargar historial de modelos"):
    try:
        response = requests.get(f"{API_URL}/model-history")
        response.raise_for_status()
        history = response.json()

        if not history:
            st.info("No hay modelos en el historial.")
        else:
            for run in history:
                st.subheader(f"Run ID: {run['run_id']}")
                st.write(f"🕒 **Fecha**: {run['start_time']}")
                st.write(f"🔁 **Estado de producción**: {run['status']}")
                st.write(f"📉 **MAE**: {run.get('mae', 'N/A'):.2f}")
                st.write(f"📏 **MSE**: {run.get('mse', 'N/A'):.2f}")
                st.write(f"🎯 **R2 Score**: {run.get('r2', 'N/A'):.2f}")
                st.write(f"📊 **Parámetros**:")
                st.json(run['params'])
                if run['rejection_reason']:
                    st.write(f"❌ **Motivo de rechazo**: {run['rejection_reason']}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Error al cargar historial: {e}")

st.markdown("---")
st.header("Explicación del modelo (SHAP)")

if st.button("Mostrar explicación del modelo en producción"):
    try:
        response = requests.get(f"{API_URL}/production-plot")
        response.raise_for_status()
        data = response.json()
        img_bytes = base64.b64decode(data["image_base64"])
        st.image(img_bytes, caption=f"SHAP Summary - Run ID: {data['run_id']}")
    except Exception as e:
        st.error(f"No se pudo cargar la explicación: {e}")
