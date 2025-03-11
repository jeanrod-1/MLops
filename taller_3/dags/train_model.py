from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import joblib
import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier

def train_model():
    engine = create_engine("mysql+pymysql://airflow:airflow_pass@mysql:3306/airflow_db")
    
    # Cargar datos preprocesados
    df = pd.read_sql("SELECT * FROM penguins_preprocessed", engine)
    print("Datos preprocesados cargados:", df.head())
    
    features = ['bill_length_mm', 'bill_depth_mm', 'body_mass_g']
    target = 'sex'
    
    X = df[features]
    y = df[target]
    
    model = RandomForestClassifier()
    model.fit(X, y)
    
    model_dir = "/models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'rf_model.joblib')
    joblib.dump(model, model_path)
    print(f"Modelo guardado en {model_path}")

default_args = {
    'start_date': datetime(2023, 1, 1)
}

with DAG(
    'train_penguins_model',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
) as dag:

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )
