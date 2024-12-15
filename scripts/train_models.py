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

    # Entrenar modelo
    print("Entrenando modelo...")
    model = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)
    model.fit(X, y)

    # Guardar modelo
    with open(output_model, "wb") as f:
        pickle.dump(model, f)
    print(f"Modelo guardado en: {output_model}")

if __name__ == "__main__":
    # Entrenar modelos para catalog y shop items
    train_model("../data/catalog_training_data.csv", "../models/catalog_model.pkl")
    train_model("../data/shop_items_training_data.csv", "../models/shop_items_model.pkl")
