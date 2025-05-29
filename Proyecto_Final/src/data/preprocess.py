import pandas as pd, sqlalchemy as sa
import os
from config import POSTGRES, RAW_SCHEMA, CLEAN_SCHEMA

TARGET = "price"    

def _get_engine():
    c = POSTGRES
    return sa.create_engine(
        f"postgresql://{c['user']}:{c['password']}@{c['host']}:{c['port']}/{c['db']}"
    )

def transform(df: pd.DataFrame):
    y = df[TARGET]

    # Eliminar columnas no útiles (aunque numéricas): street (ID), zip_code (código), etc.
    drop_cols = ["street", "zip_code", "prev_sold_date", "brokered_by"]  # ajusta según tus datos
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # Solo usar columnas numéricas (excluyendo el target)
    X = df.drop(columns=[TARGET])
    X = X.select_dtypes(include="number")

    return X, y


def main():
    engine = _get_engine()
    df = pd.read_sql_table("house_prices", engine, schema=RAW_SCHEMA)

    X, y = transform(df)

    with engine.begin() as conn:
        conn.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {CLEAN_SCHEMA};"))
        X.to_sql("features", conn, schema=CLEAN_SCHEMA, if_exists="replace", index=False)
        pd.DataFrame({"target": y}).to_sql("labels", conn, schema=CLEAN_SCHEMA, if_exists="replace", index=False)

    print("Proceso CLEAN completo")

if __name__ == "__main__":
    main()
