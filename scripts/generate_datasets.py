import xml.etree.ElementTree as ET
import pandas as pd

def traverse_tree_and_collect_data(file_path, output_csv, file_type):
    """Recorre un árbol XML y recolecta datos para entrenamiento."""
    print(f"Procesando archivo: {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = []
    def collect_data(node, depth=0):
        # Recolectar características y etiqueta
        data.append({
            "depth": depth,
            "num_children": len(list(node)),
            "num_attributes": len(node.attrib),
            "tag": node.tag,  # Etiqueta real (ground truth)
        })
        for child in node:
            collect_data(child, depth + 1)

    collect_data(root)
    
    # Convertir a DataFrame y guardar
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Datos guardados en: {output_csv}")

if __name__ == "__main__":
    # Archivos de entrada
    archivos_catalog = [
        "../data/whyems_catalog.ymt",
        "../data/red_dead_offline_catalog.ymt"
    ]
    archivos_shop_items = [
        "../data/whyems_shop_items.ymt",
        "../data/red_dead_offline_shop_items.ymt"
    ]

    # Generar datasets
    for file_path in archivos_catalog:
        traverse_tree_and_collect_data(file_path, "../data/catalog_training_data.csv", "catalog")
    
    for file_path in archivos_shop_items:
        traverse_tree_and_collect_data(file_path, "../data/shop_items_training_data.csv", "shop_items")
