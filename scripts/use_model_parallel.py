import os
import pickle
import xml.etree.ElementTree as ET
from collections import defaultdict
import copy
import pandas as pd
import math

# Límites basados en los reportes
LIMITS = {
    "item": 300000,
    "abs": 27000,
    "purge": 27000,
    "linkshopid": 15000,
    "linkmenuid": 15000,
}

def load_model(model_path):
    """Carga el modelo entrenado desde el archivo .pkl."""
    with open(model_path, "rb") as f:
        return pickle.load(f)

def process_nodes_in_batches(model, nodes, batch_size, progress_step=100):
    """Procesa nodos en lotes y realiza predicciones."""
    predictions = []
    total_batches = math.ceil(len(nodes) / batch_size)

    for batch_index in range(total_batches):
        batch = nodes[batch_index * batch_size:(batch_index + 1) * batch_size]
        data = pd.DataFrame(
            [[node["depth"], node["num_children"], len(node["attributes"])] for node in batch],
            columns=["depth", "num_children", "num_attributes"]
        )
        batch_predictions = model.predict(data)
        predictions.extend(batch_predictions)

        if (batch_index + 1) % progress_step == 0 or batch_index + 1 == total_batches:
            print(f"Lote {batch_index + 1}/{total_batches} procesado...")

    return predictions

def traverse_tree_with_depth(root):
    """Recorre un árbol XML y devuelve una lista de nodos con características."""
    nodes = []
    def collect_nodes(node, depth=0):
        nodes.append({
            "depth": depth,
            "tag": node.tag,
            "num_children": len(list(node)),
            "attributes": list(node.attrib.keys()),
            "node": node
        })
        for child in node:
            collect_nodes(child, depth + 1)
    collect_nodes(root)
    return nodes

def eliminar_duplicados(root):
    """Elimina nodos duplicados basándose en etiquetas y atributos."""
    vistos = set()
    for parent in root.findall(".//*"):
        for child in list(parent):
            clave = (child.tag, ET.tostring(child, encoding="unicode"))
            if clave in vistos:
                parent.remove(child)
            else:
                vistos.add(clave)

def fusionar_archivos(model, original_file, nuevo_file, output_file, bug_report, batch_size):
    """Fusiona archivos XML respetando límites, eliminando duplicados y generando un bug report."""
    print("Cargando y procesando archivo original...")
    tree_original = ET.parse(original_file)
    root_original = tree_original.getroot()
    original_nodes = traverse_tree_with_depth(root_original)

    print("Cargando y procesando archivo nuevo...")
    tree_nuevo = ET.parse(nuevo_file)
    root_nuevo = tree_nuevo.getroot()
    nuevo_nodes = traverse_tree_with_depth(root_nuevo)

    print("Realizando predicciones para los nodos del archivo nuevo...")
    predictions = process_nodes_in_batches(model, nuevo_nodes, batch_size)

    print("Fusionando nodos...")
    predicted_structure = defaultdict(list)
    stats = defaultdict(int)

    for feature, prediction in zip(nuevo_nodes, predictions):
        predicted_structure[prediction].append(feature["node"])
        stats[feature["tag"]] += 1

    for prediction, nodes in predicted_structure.items():
        target_node = root_original.find(f".//{prediction}")
        if target_node is not None:
            for node in nodes:
                if stats[node.tag] <= LIMITS.get(node.tag, float("inf")):
                    target_node.append(copy.deepcopy(node))
                else:
                    print(f"Advertencia: Límite excedido para <{node.tag}>.")
        else:
            generic_section = root_original.find(".//GenericUnmergedNodes")
            if generic_section is None:
                generic_section = ET.SubElement(root_original, "GenericUnmergedNodes")
            for node in nodes:
                if stats[node.tag] <= LIMITS.get(node.tag, float("inf")):
                    generic_section.append(copy.deepcopy(node))

    print("Eliminando duplicados...")
    eliminar_duplicados(root_original)

    print("Generando bug report...")
    with open(bug_report, "w", encoding="utf-8") as report:
        report.write("Reporte del proceso de fusión\n")
        report.write("=" * 50 + "\n")
        for tag, count in stats.items():
            report.write(f"<{tag}> creados: {count}\n")
    print(f"Bug report generado en: {bug_report}")

    print("Guardando archivo fusionado...")
    tree_original.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Archivo fusionado guardado en: {output_file}")

if __name__ == "__main__":
    tipo_archivo = input("¿Qué tipo de archivo estás procesando? (catalog/shop_items): ").strip().lower()

    if tipo_archivo == "catalog":
        model_path = "../models/catalog_model.pkl"
        original_file = "../data/whyems_catalog.ymt"
        nuevo_file = "../data/red_dead_offline_catalog.ymt"
        output_file = "../data/fused_catalog.ymt"
        bug_report = "../reports/fused_catalog_report.txt"
    elif tipo_archivo == "shop_items":
        model_path = "../models/shop_items_model.pkl"
        original_file = "../data/whyems_shop_items.ymt"
        nuevo_file = "../data/red_dead_offline_shop_items.ymt"
        output_file = "../data/fused_shop_items.ymt"
        bug_report = "../reports/fused_shop_items_report.txt"
    else:
        raise ValueError("Tipo de archivo no reconocido.")

    print("Cargando el modelo entrenado...")
    model = load_model(model_path)
    fusionar_archivos(model, original_file, nuevo_file, output_file, bug_report, batch_size=1000)
