from getGpcCodes import gpc_by_file
from gs1Api import trade_items_by_gpc, trade_items_by_date
from batchesProcessing import create_batch
from dataprocessing import read_json, flatten_json, read_files,process_files,move_files
from queries import fetch_atributos
import datetime,json, time

if __name__ == "__main__":
    connection="Driver={SQL Server Native Client 11.0};Server=CCAZR-PROC01\PROC_cirugias;Database=ISCAM_GS1;Uid=UsrInovacion;Pwd=M4ryW1tch041123!;"

    file_name="GPC.json"
    start_date="2017-01-01"
    today=datetime.datetime.today()
    end_date=today.strftime("%Y-%m-%d")
    
    # => Leer los GPC y guardarlos en batches
    with open(file_name,'r',encoding='utf-8') as jsonfile:
        gpc_data=json.load(jsonfile)

    for i,gpc in enumerate(gpc_data):
        print("="*50)
        print(f"{i}/{len(gpc_data)} -- GPC {gpc}")
        lista_items=trade_items_by_gpc(gpc,start_date,end_date)
        if lista_items:
            
            create_batch(gpc,lista_items)
        

    

    