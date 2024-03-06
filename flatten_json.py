import json,csv


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], f"{name}{a}.")
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, f"{name}{i}.")
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def flatten_noDup_json(y):
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

def create_attributes(attribute_list, file_name='attributes.csv'):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_atributo', 'atributo_nombre'])
        
        for id, attribute in enumerate(attribute_list, start=1):
            writer.writerow([id, attribute])

if __name__=="__main__":
    with open('items_api.json', 'r',encoding='utf-8') as f:
        data = json.load(f)

    flat_data = flatten_noDup_json(data)
    flat_fields = list(flat_data.keys())

    print(len(flat_fields))
    create_attributes(flat_fields, 'attributes_api.csv')
    
        
    with open(r'.\examples\raw_example.json', 'r') as f:
        data = json.load(f)

    flat_data = flatten_noDup_json(data)
    flat_fields = list(flat_data.keys())

    print(len(flat_fields))
    create_attributes(flat_fields, 'attributes_web.csv')

    
    