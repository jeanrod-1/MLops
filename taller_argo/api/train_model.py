import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os


df = pd.read_csv("diabetic_data.csv")

# Paso 2: Preprocesamiento
# Eliminamos columnas con demasiados valores únicos o irrelevantes
drop_cols = [
    'encounter_id', 'patient_nbr','payer_code','diag_1', 'diag_2', 'diag_3'
]
df = df.drop(columns=drop_cols)

# Reemplazar "?" por NaN
df = df.replace("?", pd.NA)

# Eliminar columnas con más del 50% de valores faltantes
null_threshold = 0.5
df = df.loc[:, df.isnull().mean() < null_threshold]

# Eliminar filas que aún tengan nulos
df = df.dropna()


# Convertimos la columna objetivo a binaria
df['readmitted'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)

# Codificamos variables categóricas
le = LabelEncoder()
for col in df.select_dtypes(include=['object']).columns:
    df[col] = le.fit_transform(df[col])

# Paso 3: División de datos
X = df.drop('readmitted', axis=1)
y = df['readmitted']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Paso 4: Entrenamiento del modelo
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Paso 5: Evaluación
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Paso 6: Guardar modelo
joblib.dump(clf, "app/model.pkl")
print("Modelo entrenado y guardado en app/model.pkl")