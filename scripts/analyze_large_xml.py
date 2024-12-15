import xml.etree.ElementTree as ET
from collections import defaultdict

def analyze_large_xml(file_path, output_summary, block_size=10000):
    """
    Analiza un archivo XML grande en bloques y genera un resumen de los nodos.
    Args:
        file_path (str): Ruta al archivo XML.
        output_summary (str): Ruta al archivo de resumen.
        block_size (int): Número de nodos procesados por bloque.
    """
    print(f"Analizando archivo: {file_path}")
    try:
        context = ET.iterparse(file_path, events=("start", "end"))
        node_counts = defaultdict(int)
        current_block = 0
        total_nodes = 0

        with open(output_summary, "w", encoding="utf-8") as summary_file:
            summary_file.write(f"Resumen del archivo: {file_path}\n")
            summary_file.write("=" * 50 + "\n")

            for event, elem in context:
                if event == "start":
                    node_counts[elem.tag] += 1
                    total_nodes += 1

                    if total_nodes % block_size == 0:
                        current_block += 1
                        summary_file.write(f"\n--- Bloque {current_block} ---\n")
                        for tag, count in node_counts.items():
                            summary_file.write(f"{tag}: {count}\n")
                        node_counts.clear()

                # Limpia elementos ya procesados para reducir uso de memoria
                if event == "end":
                    elem.clear()

            # Escribir el último bloque
            if node_counts:
                current_block += 1
                summary_file.write(f"\n--- Bloque {current_block} ---\n")
                for tag, count in node_counts.items():
                    summary_file.write(f"{tag}: {count}\n")

            summary_file.write("\nTotal de nodos procesados: {}\n".format(total_nodes))

        print(f"Resumen generado en: {output_summary}")
    except Exception as e:
        print(f"Error al analizar el archivo: {e}")

if __name__ == "__main__":
    # Rutas de los archivos XML
    files_to_analyze = [
        "../data/whyems_catalog.ymt",
        "../data/red_dead_offline_catalog.ymt",
        "../data/fused_catalog.ymt"
    ]

    for file_path in files_to_analyze:
        output_summary = file_path.replace(".ymt", "_summary.txt")
        analyze_large_xml(file_path, output_summary)
