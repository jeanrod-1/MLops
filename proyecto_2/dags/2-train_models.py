from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

# Configuración básica del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'train_models_dag',
    default_args=default_args,
    description='DAG para entrenar modelos y registrar en MLflow',
    schedule_interval='@once',
)

# Función para entrenar modelos
def train_models():
    df = pd.read_csv('/tmp/data.csv')
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='linear', probability=True, random_state=42)
    }
    
    mlflow.set_tracking_uri("http://10.43.101.193:5000")
    for name, model in models.items():
        with mlflow.start_run():
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)
            mlflow.log_param("model_name", name)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.sklearn.log_model(model, name)

# Operador de Airflow
task_train_models = PythonOperator(
    task_id='train_models',
    python_callable=train_models,
    dag=dag,
)
