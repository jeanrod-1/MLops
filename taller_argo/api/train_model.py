import pickle
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

def train_and_save():
    iris = load_iris()
    model = RandomForestClassifier()
    model.fit(iris.data, iris.target)
    os.makedirs("app", exist_ok=True)
    with open("app/model.pkl", "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train_and_save()