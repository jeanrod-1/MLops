from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

from scripts.preprocess import preprocess_data
from scripts.train import train_model

RAW_PATH = 'data/raw/data.csv'
CLEAN_PATH = 'data/clean/clean_data.csv'


def extract():
    import pandas as pd
    
    df = pd.read_csv('https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv')
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv(RAW_PATH, index=False)


def validate():
    
    return True # o False


def train():
    if validate():
        train_model(CLEAN_PATH)

with DAG('housing_pipeline', start_date=datetime(2023, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    t1 = PythonOperator(task_id='extract_data', python_callable=extract)
    t2 = PythonOperator(task_id='preprocess_data', python_callable=lambda: preprocess_data(RAW_PATH, CLEAN_PATH))
    t3 = PythonOperator(task_id='train_model', python_callable=train)

    t1 >> t2 >> t3