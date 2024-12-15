import os
import re
import pandas as pd

def parse_report(file_path):
    """Parsea un reporte y extrae información de nodos y atributos."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Buscar líneas con el formato "<tag> encontrados: count"
            match = re.match(r"<(\w+)> encontrados: (\d+)", line)
            if match:
                tag, count = match.groups()
                data.append({"tag": tag, "count": int(count)})
    return pd.DataFrame(data)

def generate_dataset(report_paths, output_csv):
    """Genera un dataset de entrenamiento basado en los reportes."""
    all_data = []
    for report_path in report_paths:
        print(f"Procesando reporte: {report_path}")
        df = parse_report(report_path)
        print("Datos procesados del reporte:")
        print(df.head())  # Imprime las primeras filas para verificar
        all_data.append(df)

    # Combinar datos de múltiples reportes
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
    else:
        raise ValueError("No se encontraron datos en los reportes.")

    print("Datos combinados (antes de agrupar):")
    print(combined_df.head())  # Verifica el DataFrame combinado

    # Agrupar por `tag` y sumar los conteos
    combined_df = combined_df.groupby("tag").sum().reset_index()

    # Agregar columnas ficticias para entrenamiento
    combined_df["depth"] = combined_df["count"] % 10  # Datos simulados
    combined_df["num_children"] = combined_df["count"] // 10
    combined_df["num_attributes"] = combined_df["count"] % 5

    print("Datos listos para guardar:")
    print(combined_df.head())  # Verifica los datos finales antes de guardar

    # Guardar como CSV
    combined_df[["depth", "num_children", "num_attributes", "tag"]].to_csv(output_csv, index=False)
    print(f"Dataset guardado en: {output_csv}")

if __name__ == "__main__":
    # Rutas de los reportes
    catalog_reports = [
        "../reports/whyem's_catalog_report.txt",
        "../reports/red_dead_offline_catalog_report.txt"
    ]
    shop_items_reports = [
        "../reports/whyem's_shop_items_report.txt",
        "../reports/red_dead_offline_shop_items_report.txt"
    ]

    # Generar datasets
    generate_dataset(catalog_reports, "../data/catalog_training_data.csv")
    generate_dataset(shop_items_reports, "../data/shop_items_training_data.csv")
