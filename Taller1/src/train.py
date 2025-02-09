import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_model():
    data = pd.read_csv('data/processed_penguins.csv')

    features = ['culmen_length_mm', 'culmen_depth_mm', 'body_mass_g'] 
    target = 'Species'

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f'Accuracy: {accuracy:.2f}')

    joblib.dump(model, 'model.joblib')
    print("Modelo guardado en model.joblib")

if __name__ == "__main__":
    train_model()