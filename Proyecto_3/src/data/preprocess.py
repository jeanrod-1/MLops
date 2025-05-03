import pandas as pd, sqlalchemy as sa
from sklearn.preprocessing import OneHotEncoder
import joblib, os
from config import POSTGRES, RAW_SCHEMA, CLEAN_SCHEMA

TARGET = "readmitted"    

def _get_engine():
    c = POSTGRES
    return sa.create_engine(
        f"postgresql://{c['user']}:{c['password']}@{c['host']}:{c['port']}/{c['db']}"
    )

def transform(df: pd.DataFrame):
    y = (df[TARGET] == "<30").astype(int)

    # Eliminar columnas que contienen "diag" en el nombre
    df = df.drop(columns=[col for col in df.columns if "diag" in col])

    # Eliminar columnas que no se deben usar como features
    X = df.drop(columns=[TARGET, "encounter_id", "patient_nbr"])

    # Identificar columnas categóricas
    cat_cols = X.select_dtypes("object").columns

    # One-Hot Encoding
    ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    X_ohe = ohe.fit_transform(X[cat_cols])

    # Crear DataFrame final combinando OHE + numéricas
    X_final = pd.concat(
        [pd.DataFrame(X_ohe, columns=ohe.get_feature_names_out(cat_cols)), 
         X.drop(columns=cat_cols).reset_index(drop=True)],
        axis=1
    )

    return X_final, y, ohe


def main():
    engine = _get_engine()
    df = pd.read_sql_table("diabetes", engine, schema=RAW_SCHEMA)

    X, y, ohe = transform(df)

    with engine.begin() as conn:
        conn.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {CLEAN_SCHEMA};"))
        X.to_sql("features", conn, schema=CLEAN_SCHEMA, if_exists="replace", index=False)
        y.to_frame("target").to_sql("labels", conn, schema=CLEAN_SCHEMA, if_exists="replace", index=False)

    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(ohe, "artifacts/ohe.joblib")
    print("Proceso CLEAN completo")

if __name__ == "__main__":
    main()