from dataprocessing import save_json
import os, datetime


def create_batch(gpc,data):
    fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")

    script_dir = os.path.dirname(os.path.realpath(__file__))  # Directorio del script
    root = os.path.join(script_dir, "atributtesBatches")  # Construir la ruta del directorio
    if not os.path.exists(root):
        os.makedirs(root)  # Crear el directorio si no existe
    file_name = os.path.join(root, f"{gpc}_batch_{fecha_actual}.json")  # Construir la ruta del archivo
    save_json(data, file_name)

def split_batch(batch):
    pass