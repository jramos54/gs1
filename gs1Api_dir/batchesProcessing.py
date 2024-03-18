from dataprocessing import save_json
import os

def create_batch(gpc,data):
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Directorio del script
    root = os.path.join(script_dir, "atributtesBatches")  # Construir la ruta del directorio
    if not os.path.exists(root):
        os.makedirs(root)  # Crear el directorio si no existe
    file_name = os.path.join(root, f"{gpc}_batch.json")  # Construir la ruta del archivo
    save_json(data, file_name)

def split_batch(batch):
    pass