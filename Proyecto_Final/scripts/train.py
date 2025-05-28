import pandas as pd
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def train_model(data_path):
    df = pd.read_csv(data_path)
    X = df.drop("median_house_value", axis=1)
    y = df["median_house_value"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_metric("mse", mse)
        mlflow.set_tag("stage", "production")