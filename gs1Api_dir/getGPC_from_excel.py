import pandas as pd
import json

def get_unique_values(archivo_excel):
    # Leer el archivo Excel
    df = pd.read_excel(archivo_excel)
    
    # Verificar si la columna 'BrickCode' está en el DataFrame
    if 'BrickCode' in df.columns:
        # Obtener los valores únicos de la columna 'BrickCode'
        valores_unicos = df['BrickCode'].unique()
        return valores_unicos
    else:
        return "La columna 'BrickCode' no se encuentra en el archivo."


if __name__=="__main__":
    file_name="GPC.xlsx"
    gpcs=get_unique_values(file_name)
    print(len(gpcs))
    gpcs_lista = gpcs.tolist()

    with open("GPC.json", 'w') as json_file:
        json.dump(gpcs_lista, json_file)
