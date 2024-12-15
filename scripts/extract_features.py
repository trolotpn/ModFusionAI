import os
import xml.etree.ElementTree as ET
import json

def extract_features_from_xml(file_path):
    """Extrae características jerárquicas de un archivo XML."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        features = []

        def traverse_tree(node, depth=0):
            # Extraer características de cada nodo
            tag = node.tag
            num_children = len(list(node))
            attributes = list(node.attrib.keys())
            features.append({
                "depth": depth,
                "tag": tag,
                "num_children": num_children,
                "attributes": attributes
            })

            # Recursivamente procesar los hijos
            for child in node:
                traverse_tree(child, depth + 1)

        traverse_tree(root)
        return features
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return []

def process_folder(folder_path, output_file):
    """Procesa todos los archivos XML en una carpeta y guarda sus características en JSON."""
    all_features = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xml") or file_name.endswith(".ymt"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Procesando archivo: {file_name}")
            features = extract_features_from_xml(file_path)
            all_features[file_name] = features

    # Guardar las características en un archivo JSON
    with open(output_file, "w") as f:
        json.dump(all_features, f, indent=4)
    print(f"Características extraídas guardadas en: {output_file}")

if __name__ == "__main__":
    # Ruta de la carpeta donde están los archivos XML
    input_folder = "../data"
    output_file = "../data/features.json"

    process_folder(input_folder, output_file)
