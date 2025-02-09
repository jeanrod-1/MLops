import pandas as pd

def load_data():
    df_iter = pd.read_csv('data/penguins_lter.csv')
    df_size = pd.read_csv('data/penguins_size.csv')
    return df_iter, df_size

def preprocess_data(df_iter, df_size):
    df_iter = df_iter.dropna()

    df_iter = df_iter.rename(columns={
        "Culmen Length (mm)": "culmen_length_mm",
        "Culmen Depth (mm)": "culmen_depth_mm",
        "Body Mass (g)": "body_mass_g"
    })

    return df_iter

if __name__ == "__main__":
    df_iter, df_size = load_data()
    processed_data = preprocess_data(df_iter, df_size)
    
    processed_data.to_csv('data/processed_penguins.csv', index=False)