import os, traceback, time, json,csv
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def read_excel(file_path):
 
    try:
        df = pd.read_excel(file_path, sheet_name='Entities', skiprows=1)
        if 'Information provider GLN' in df.columns:
            gln_list = df['Information provider GLN'].tolist()
            return gln_list
        else:
            print(f"La columna 'Information provider GLN' no está presente en el archivo {file_path}")
            return []
    except Exception as e:
        print(f"No se pudo leer el archivo {file_path}: {e}")
        return []

def get_gln(directorio):
    gln_total = []
    for archivo in os.listdir(directorio):
        if archivo.endswith('.xlsm'):
            archivo_path = os.path.join(directorio, archivo)
            gln_list = read_excel(archivo_path)
            gln_total.extend(gln_list)
    return gln_total


def get_total_products(gln):
    
    url = "https://apisync.syncfonia.com/wsproxy/apiservices/tradeItemService.svc/GetProducts"

    username = os.getenv("USER")
    password = os.getenv("PASSWORD")

    headers = {
        "Content-Type": "application/json",
        
    }
    payload = {
        "Gln": gln
    }    
    
    if username and password:
        try:
            response = requests.post(url, json=payload, headers=headers, auth=(username,password))
            data = response.json()
            print(data)
            if response.status_code == 200:
                return int(data.get('TotalProducts', 0))
            else:
                print(f"Error al obtener el número total de productos. Código de estado: {response.status_code}")
                return 0
        except Exception as e:
            print(f"Error al conectarse a la API: {e}")
            return 0
    else:
        print("No se encontraron las credenciales de autenticación en el archivo .env")
        return 0

def trade_items(gln):
   
    url = "https://apisync.syncfonia.com/wsproxy/apiServices/tradeItemService.svc/Search"
    page_number = 1
    page_size = 50
    total_elements = []
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")

    headers = {
        "Content-Type": "application/json",
    }

    while True:
        payload = {
            "TradeItemKey": {
                "Gln": gln,
                "TargetMarketCountryCode": "484"
            },
            "Gpc": 10001961,
            "PageNumber": page_number,
            "PageSize": page_size,
            "TradeItemModules": ["ALL"]
        }

        try:
            response = requests.post(url, json=payload, headers=headers, auth=(username, password))
            data = response.json()
            if response.status_code == 200:
                if data.get("Errors") is None:
                    trade_item_list = data.get('TradeItemList', [])
                    print(f"total elements : {len(trade_item_list)}")
                    total_elements.extend(trade_item_list)
                    page_number += 1
                else:
                    print(f"La paginación ha finalizado.\n{data.get('Errors')}")
                    break
            else:
                print(f"Error al consumir la API. Código de estado: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a la API: {e}")
            break

    return total_elements

def save_dict_list_to_json(dict_list, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(dict_list, file, ensure_ascii=False, indent=4)
        

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

def create_attributes(attributes, file_name='attributes_api.csv'):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_atributo', 'atributo_nombre'])
        
        for id, attribute in enumerate(attributes, start=1):
            writer.writerow([id, attribute])        
        
         
def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_product_csv(product_attributes, file_name='productos_api.csv'):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_producto', 'id_atributo', 'valor_atributo'])

        for id_producto, attributes in product_attributes.items():
            for id_atributo, valor_atributo in attributes.items():
                writer.writerow([id_producto, id_atributo, valor_atributo])

def create_product_attributes(data, file_name='productos_api.csv', attributes_file='attributes_api.csv'):
    # Función para cargar attribute_ids desde un archivo CSV
    def load_attribute_ids(filename):
        attribute_ids = {}
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la fila del encabezado
            for row in reader:
                attribute_ids[row[1]] = row[0]
        return attribute_ids

    # Función para aplanar el JSON y escribir en el archivo CSV
    def flatten_and_write(item, writer, gtin, attribute_ids):
        def flatten(x, name=''):
            if isinstance(x, dict):
                for a in x:
                    flatten(x[a], f"{name}{a}.")
            elif isinstance(x, list):
                for a in x:
                    if isinstance(a, (dict, list)):
                        flatten(a, name)
            else:
                attr_name = name[:-1]
                if attr_name in attribute_ids:
                    value = "NA" if x is None else x  # Convertir None a "NA"
                    writer.writerow([gtin, attribute_ids[attr_name], value])

        flatten(item)

    # Cargar attribute_ids desde el archivo
    attribute_ids = load_attribute_ids(attributes_file)

    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['GTIN', 'id_atributo', 'valor_atributo'])

        for item in data:
            gtin = item.get('GTIN')
            if gtin:
                flatten_and_write(item, writer, gtin, attribute_ids)

if __name__=="__main__":
    
    directorio_archivos = r'C:\Users\jramos\codingFiles\dacodes\gs1_project\excel_files'
    gln_total = get_gln(directorio_archivos)
    glns=set(gln_total)
    item_list=[]
    gln_special=None
    for gln in glns:  
        print(f"items for GLN : {gln}")      
        item_products= trade_items(gln)
        time.sleep(6)
        print(len(item_products))
        item_list.extend(item_products)    
    save_dict_list_to_json(item_list,"items_api.json")

    with open('items_api.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    flat_data = flatten_json(data)
    attribute_list = list(set(flat_data.keys()))
    create_attributes(attribute_list)
    attribute_ids = {attr: idx+1 for idx, attr in enumerate(attribute_list)}
    create_product_attributes(data)

    
    
   
        

