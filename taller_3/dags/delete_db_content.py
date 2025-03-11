from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1)
}

with DAG(
    'delete_db_content',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
) as dag:

    delete_tables = MySqlOperator(
        task_id='truncate_penguins_tables',
        mysql_conn_id='mysql_default', ##Cambiar por el id
        sql=[
            "DROP TABLE IF EXISTS penguins_raw;",
            "DROP TABLE IF EXISTS penguins_preprocessed;"
        ]

    )