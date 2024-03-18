from dataprocessing import read_json
import json

def get_gpc_codes(data, result=None):
    if result is None:
        result = {}

    for item in data:
        level_key = f"level{item['Level']}"
        code = item['Code']

        # Agregar el código al nivel correspondiente
        if level_key not in result:
            result[level_key] = []
        result[level_key].append(code)

        # Llamada recursiva si hay hijos
        if 'Childs' in item and item['Childs']:
            get_gpc_codes(item['Childs'], result)

    return result

def gpc_by_file(file_name):
    data=read_json(file_name)
    gpc_codes=get_gpc_codes(data["Schema"])
    
    return gpc_codes

if __name__=="__main__":
    file_name="GPC_raw.json"
    codes=gpc_by_file(file_name)
    
    for level in codes.keys():
        
        print(f"{level} contains {len(codes.get(level))} codes")
    #print(json.dumps(codes,indent=4))