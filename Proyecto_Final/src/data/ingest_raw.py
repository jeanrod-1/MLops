"""
Consulta datos desde API y los inserta en Postgres (esquema RAW)
"""

import requests
import pandas as pd
import sqlalchemy as sa
from config import POSTGRES, RAW_SCHEMA

# URL del endpoint
API_URL = "http://10.43.101.108:80/data"
API_RESTART_URL = "http://10.43.101.108:80/restart_data_generation"

# Parámetros del GET
PARAMS = {
    "group_number": 6,
    "day": "Tuesday"
}

def get_engine():
    creds = POSTGRES
    return sa.create_engine(
        f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['db']}"
    )

def fetch_data_from_api() -> pd.DataFrame:

    try:
        r = requests.get(API_URL, params=PARAMS)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return None
    
    # Arreglamos el caso en que haya un carácter o coma al principio que impida el parseo
    text = r.text.strip()
    if text.startswith(","):
        text = text[1:]  # Remueve coma inicial si existe

    try:
        data = pd.read_json(text)
    except ValueError:
        try:
            data = pd.read_json(r.content)
        except ValueError as e:
            print(f"Error al parsear JSON: {e}")
            return None
        
    if "data" not in data:
        print("No más data por procesar")
        return None
    
    df = data["data"].apply(pd.Series)
    if df.empty:
        print("No más data por procesar")
        return None
    
    return df

def main():

    # r = requests.get(API_RESTART_URL, params=PARAMS)
    # print(r)

    df = fetch_data_from_api()
    if df is None:
        # Si no hay datos o hubo error, terminamos sin fallo
        return
    
    print(df.head())
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA};"))

    df.to_sql("house_prices", engine, schema=RAW_SCHEMA,
              if_exists="replace", index=False, method="multi")
    print("Carga RAW completa")

if __name__ == "__main__":
    main()
