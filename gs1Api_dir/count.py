import os, json

def sum_list_sizes_in_json_files(directory):
    total_size = 0

    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directory):
        # Verifica si es un archivo JSON
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            
            # Lee el archivo JSON
            with open(filepath, 'r') as file:
                data = json.load(file)
                
                # Suma el tamaño de todas las listas en el archivo
                # for key, value in data.items():
                #     if isinstance(value, list):
                #         total_size += len(value)
                print(len(data))
    
    return total_size

if __name__=="__main__":
    directory="atributtesBatches"
    sum_list_sizes_in_json_files(directory)