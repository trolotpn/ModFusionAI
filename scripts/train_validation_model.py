import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

def train_model(input_csv, output_model):
    """Entrena un modelo Random Forest basado en los datos de entrada."""
    print(f"Cargando datos de: {input_csv}")
    data = pd.read_csv(input_csv)

    # Separar características y etiquetas
    X = data[["depth", "num_children", "num_attributes"]]
    y = data["tag"]

    print("Entrenando modelo de validación...")
    model = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)
    model.fit(X, y)

    with open(output_model, "wb") as f:
        pickle.dump(model, f)
    print(f"Modelo guardado en: {output_model}")

if __name__ == "__main__":
    train_model("../data/validation_training_data.csv", "../models/validation_model.pkl")
