from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner": "mlops", "retries": 1}

with DAG("diabetes_pipeline",
         default_args=default_args,
         schedule_interval="@daily",
         start_date=datetime(2023, 1, 1),
         catchup=False) as dag:

    ingest = BashOperator(
        task_id="ingest_raw",
        bash_command="PYTHONPATH=/opt/airflow/src python /opt/airflow/src/data/ingest_raw.py"
    )

    preprocess = BashOperator(
        task_id="preprocess",
        bash_command="PYTHONPATH=/opt/airflow/src python /opt/airflow/src/data/preprocess.py"
    )

    train = BashOperator(
        task_id="train",
        bash_command="PYTHONPATH=/opt/airflow/src python /opt/airflow/src/modeling/train.py"
    )

    select_best = BashOperator(
        task_id="evaluate_register",
        bash_command="PYTHONPATH=/opt/airflow/src python /opt/airflow/src/modeling/evaluate_register.py"
    )

    ingest >> preprocess >> train >> select_best
