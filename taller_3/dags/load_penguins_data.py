from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import shutil

def load_penguins():
    cache_dir = "/home/airflow/.cache/seaborn"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)  # Borra el caché antes de importar seaborn

    import seaborn as sns
    import pandas as pd
    from sqlalchemy import create_engine

    engine = create_engine("mysql+pymysql://airflow:airflow_pass@mysql:3306/airflow_db")

    df = sns.load_dataset("penguins")
    print("Datos originales:", df.head())

    df.to_sql("penguins_raw", con=engine, if_exists="replace", index=False)
    print("Datos de penguins cargados en la base de datos (tabla penguins_raw).")

default_args = {
    'start_date': datetime(2023, 1, 1)
}

with DAG(
    'load_penguins_data',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
) as dag:

    load_task = PythonOperator(
        task_id='load_penguins',
        python_callable=load_penguins
    )