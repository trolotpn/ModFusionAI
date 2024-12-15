import xml.etree.ElementTree as ET
from collections import defaultdict

def analyze_mod(file_path, output_report):
    """Analiza un archivo XML y genera estadísticas detalladas."""
    print(f"Analizando archivo: {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()

    stats = defaultdict(int)
    def traverse_and_count(node):
        stats[node.tag] += 1
        for child in node:
            traverse_and_count(child)

    traverse_and_count(root)

    # Escribir estadísticas en un archivo
    with open(output_report, "w", encoding="utf-8") as report:
        report.write(f"Análisis del archivo: {file_path}\n")
        report.write("="*50 + "\n")
        for tag, count in stats.items():
            report.write(f"<{tag}> encontrados: {count}\n")

    print(f"Reporte generado: {output_report}")

if __name__ == "__main__":
    # Archivos originales
    files = {
        "WhyEm's Catalog": "../data/whyems_catalog.ymt",
        "Red Dead Offline Catalog": "../data/red_dead_offline_catalog.ymt",
        "WhyEm's Shop Items": "../data/whyems_shop_items.ymt",
        "Red Dead Offline Shop Items": "../data/red_dead_offline_shop_items.ymt"
    }

    for name, path in files.items():
        output_report = f"../reports/{name.replace(' ', '_').lower()}_report.txt"
        analyze_mod(path, output_report)
