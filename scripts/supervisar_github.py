import requests
import os

# Token de GitHub configurado como variable de entorno
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN no configurado en las variables de entorno.")

# URL base del repositorio
REPO_URL = "https://api.github.com/repos/trolotpn/ModFusionAI"

# Configurar headers de autenticación
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def listar_archivos_en_repositorio():
    """Lista los archivos en la raíz del repositorio."""
    url = f"{REPO_URL}/contents"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        print("Archivos y directorios en el repositorio:")
        for item in response.json():
            tipo = "📁 Directorio" if item["type"] == "dir" else "📄 Archivo"
            print(f"{tipo}: {item['name']}")
    else:
        print(f"Error al obtener contenido del repositorio: {response.status_code}")
        print(response.text)

def obtener_commits_recientes():
    """Obtiene los commits recientes del repositorio."""
    url = f"{REPO_URL}/commits"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        print("\nCommits recientes:")
        for commit in response.json()[:5]:  # Mostrar solo los últimos 5 commits
            print(f"- {commit['commit']['message']} (Autor: {commit['commit']['author']['name']})")
    else:
        print(f"Error al obtener commits: {response.status_code}")
        print(response.text)

def supervisar_repositorio():
    """Supervisa el repositorio: lista archivos y commits recientes."""
    print("=== Supervisando el repositorio de GitHub ===")
    listar_archivos_en_repositorio()
    obtener_commits_recientes()

if __name__ == "__main__":
    supervisar_repositorio()
