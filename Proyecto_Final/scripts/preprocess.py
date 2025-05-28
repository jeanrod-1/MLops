import pandas as pd
import os

def preprocess_data(input_path, output_path):
    df = pd.read_csv(input_path)
    df = df.dropna()
    df = pd.get_dummies(df)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)