import datetime,json, os,shutil
from queries import fetch_atributos,write_atributos_sqlserver


def date_conversion(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = date - epoch
    seconds = int(delta.total_seconds() * 1000)
    converted_string = f"/Date({seconds})/"
    return converted_string


def read_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r',encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo JSON: {e}")
        return None
    
    
def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    
    
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], f"{name}{a}.")
        elif isinstance(x, list):
            for a in x:
                if isinstance(a, (dict, list)):
                    flatten(a, name)
        else:
            if name[:-1] not in out:  # Evitar duplicados
                out[name[:-1]] = x

    flatten(y)
    return out


def read_files(directorio):
    contenido_archivos = {}
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Directorio del script
    root = os.path.join(script_dir, directorio)
    
    for archivo in os.listdir(root):
        ruta_archivo = os.path.join(root, archivo)
        
        # Asegurarse de que sea un archivo y no un directorio
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r') as file:
                contenido_archivos[ruta_archivo] = file.read()

    return contenido_archivos
        
        
def move_files(origen, destino):
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Directorio del script
    destino_path = os.path.join(script_dir, destino)

    # Crear el directorio de destino si no existe
    if not os.path.exists(destino_path):
        os.makedirs(destino_path)

    files = read_files(origen)

    for file_path in files:
        # Nombre del archivo para el nuevo destino
        file_name = os.path.basename(file_path)
        destino_file_path = os.path.join(destino_path, file_name)

        # Mover el archivo
        shutil.move(file_path, destino_file_path)
        

def process_files(files, connection_string):
    db_atributos = set(fetch_atributos(connection_string))
    atributos_nuevos = set()

    for file in files:
        batch = read_json(file)
        for item in batch:
            element = flatten_json(item)
            
            for key in element.keys():
                if key not in db_atributos and key not in atributos_nuevos:
                    atributos_nuevos.add(key)

    # Inserta todos los atributos nuevos de una sola vez
    if atributos_nuevos:
        write_atributos_sqlserver(atributos_nuevos, connection_string)
        