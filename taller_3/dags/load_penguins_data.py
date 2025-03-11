from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def load_penguins():
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