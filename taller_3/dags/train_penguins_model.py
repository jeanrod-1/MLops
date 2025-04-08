from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import joblib

def train_model():
    import pandas as pd
    from sqlalchemy import create_engine
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score

    engine = create_engine("mysql+pymysql://airflow:airflow_pass@mysql:3306/airflow_db")

    df = pd.read_sql("SELECT * FROM penguins_preprocessed", engine)
    print("Datos de entrenamiento:", df.head())

    X = df.drop(columns=["species"])
    y = df["species"]
    
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo: {accuracy:.2f}")
    
    joblib.dump(model, "/home/airflow/models/penguins_model.joblib")
    print("Modelo guardado en /home/airflow/models/penguins_model.joblib")

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
        task_id="train_penguins",
        python_callable=train_model
    )