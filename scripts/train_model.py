import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

def load_features(file_path):
    """Carga las características desde el archivo JSON generado."""
    with open(file_path, "r") as f:
        data = json.load(f)

    # Convertir las características en un DataFrame
    rows = []
    for file_name, features in data.items():
        for feature in features:
            rows.append({
                "file_name": file_name,
                "depth": feature["depth"],
                "tag": feature["tag"],
                "num_children": feature["num_children"],
                "num_attributes": len(feature["attributes"])
            })
    return pd.DataFrame(rows)

def train_model(data_file, output_model):
    """Entrena un modelo basado en las características extraídas."""
    # Cargar las características
    df = load_features(data_file)

    # Convertir las etiquetas categóricas ("tag") a números
    df["tag"] = df["tag"].astype("category").cat.codes

    # Separar características (X) y etiquetas (y)
    X = df[["depth", "num_children", "num_attributes"]]
    y = df["tag"]

    # Dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar un modelo Random Forest
    print("Entrenando modelo...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluar el modelo
    print("Evaluando modelo...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Guardar el modelo entrenado
    with open(output_model, "wb") as f:
        pickle.dump(model, f)
    print(f"Modelo guardado en: {output_model}")

if __name__ == "__main__":
    # Ruta del archivo de características
    data_file = "../data/features.json"
    # Nombre del archivo donde se guardará el modelo
    output_model = "../models/structure_model.pkl"

    train_model(data_file, output_model)
