from getGpcCodes import gpc_by_file
from gs1Api import trade_items_by_gpc
from batchesProcessing import create_batch
from dataprocessing import read_json, flatten_json, read_files,process_files,move_file
from queries import fetch_atributos,write_producto_sqlserver,fetch_atributo_id,write_productos_batch
import datetime,json

if __name__ == "__main__":
    connection="Driver={SQL Server Native Client 11.0};Server=CCAZR-PROC01\PROC_cirugias;Database=ISCAM_GS1;Uid=UsrInovacion;Pwd=M4ryW1tch041123!;"

    file_name="GPC_raw.json"
    start_date="2017-01-01"
    today=datetime.datetime.today()
    end_date=today.strftime("%Y-%m-%d")
    
    # => Leer los batches para guardar en la BD
    
    files=read_files("itemsBatches")
    for file in files:
        datas=read_json(file)
        for data in datas:
            products_insert=[]
            item=flatten_json(data)
            GTIN=item.get("GTIN",None)
            print(GTIN)
            
            for key, value in item.items():
                if value != None:
                    id_atributo = fetch_atributo_id(connection,key)
                    print(f"{id_atributo} - {key} - {value}")
                    products_insert.append((GTIN, id_atributo, value))
            write_productos_batch(products_insert,connection)
        move_file(file,"itemsBatches","obsoletes")
    
    

    