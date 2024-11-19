import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def descargar_imagen(url, carpeta):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            nombre_archivo = os.path.join(carpeta, url.split("/")[-1].split("?")[0])  # Limpia el nombre del archivo
            with open(nombre_archivo, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Imagen descargada: {nombre_archivo}")
        else:
            print(f"Error al descargar {url}")
    except Exception as e:
        print(f"Error: {e}")

def descargar_tablero_pinterest(url_tablero, carpeta_destino):
    try:
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
    except Exception as e:
        print(f"No se pudo crear la carpeta destino: {e}")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url_tablero, headers=headers)
    if response.status_code != 200:
        print("No se pudo acceder al tablero. Verifica la URL.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Busca imágenes en diferentes formatos
    imagenes = soup.find_all('img')
    print(f"Se encontraron {len(imagenes)} imágenes en el tablero.")

    for img in imagenes:
        img_url = None

        # Intenta obtener la URL de alta calidad desde varios atributos
        if img.get('data-src'):
            img_url = img.get('data-src')
        elif img.get('srcset'):
            img_url = img.get('srcset').split(",")[-1].split(" ")[0]  # Última versión del srcset
        elif img.get('src'):
            img_url = img.get('src')

        if img_url:
            img_url = urljoin(url_tablero, img_url.split("?")[0])  # Limpia parámetros de baja calidad
            print(f"Descargando imagen desde: {img_url}")
            descargar_imagen(img_url, carpeta_destino)
        else:
            print("No se encontró una URL válida para esta imagen.")

# Ejemplo de uso
url_tablero = "https://www.pinterest.com/mibullfire/fotos-con-modelo/"  # Sustituye por tu URL
carpeta_destino = "./imagenes_pinterest"
descargar_tablero_pinterest(url_tablero, carpeta_destino)