from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

# Configuración básica del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'get_data',
    default_args=default_args,
    schedule_interval='@once',
    description='DAG para recolectar datos desde la API'
)

# Función para recolectar datos
def fetch_data():
    response = requests.get('http://10.43.101.193:8000/data?group_number=6')
    data = response.json()['data']
    df = pd.DataFrame(data)
    df.to_csv('/tmp/data.csv', index=False)

# Operador de Airflow
task_fetch_data = PythonOperator(
    task_id='get_data',
    python_callable=fetch_data,
    dag=dag,
)
