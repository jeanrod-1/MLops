from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def preprocess_penguins():
    import pandas as pd
    from sqlalchemy import create_engine

    engine = create_engine("mysql+pymysql://airflow:airflow_pass@mysql:3306/airflow_db")

    df = pd.read_sql("SELECT * FROM penguins_raw", engine)
    print("Datos sin procesar:", df.head())

    df_clean = df.dropna()
    print("Datos preprocesados:", df_clean.head())

    df_clean.to_sql("penguins_preprocessed", engine, if_exists="replace", index=False)
    print("Datos preprocesados guardados en la tabla penguins_preprocessed.")

default_args = {
    'start_date': datetime(2023, 1, 1)
}

with DAG(
    'preprocess_penguins_data',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
) as dag:

    preprocess_task = PythonOperator(
        task_id="preprocess_penguins",
        python_callable=preprocess_penguins
    )