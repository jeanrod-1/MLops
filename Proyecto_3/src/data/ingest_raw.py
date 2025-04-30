"""
Descarga el archivo con la data y lo inserta en Postgres (esquema RAW)
en lotes de 15k registros.
"""

import os, requests, io, pandas as pd, sqlalchemy as sa
from config import POSTGRES, RAW_SCHEMA

URL = "https://docs.google.com/uc?export=download&id=1k5-1caezQ3zWJbKaiMULTGq-3sz6uThC"

def get_engine():
    creds = POSTGRES
    return sa.create_engine(
        f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['db']}"
    )

def download_csv() -> pd.DataFrame:
    r = requests.get(URL)
    r.raise_for_status()
    return pd.read_csv(io.BytesIO(r.content))

def main():
    df = download_csv()
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA};"))
    chunksize = 15_000
    df.to_sql("diabetes", get_engine(), schema=RAW_SCHEMA,
              if_exists="replace", index=False, chunksize=chunksize, method="multi")
    print("Carga RAW completa")

if __name__ == "__main__":
    main()