from getGpcCodes import gpc_by_file
from gs1Api import trade_items_by_gpc, trade_items_by_date
from batchesProcessing import create_batch
from dataprocessing import read_json, flatten_json, read_files,process_files,move_files
from queries import fetch_atributos
import datetime,json, time

if __name__ == "__main__":
    connection="Driver={SQL Server Native Client 11.0};Server=CCAZR-PROC01\PROC_cirugias;Database=ISCAM_GS1;Uid=UsrInovacion;Pwd=M4ryW1tch041123!;"

    file_name="GPC_raw.json"
    start_date="2017-01-01"
    today=datetime.datetime.today()
    end_date=today.strftime("%Y-%m-%d")
    
    # => Leer los GPC y guardarlos en batches
    data=gpc_by_file(file_name)
    gpc_data=data["level4"]
    
    # for gpc in gpc_data:
    #     time.sleep(2)
    #     print("="*50)
    #     print(f"GPC {gpc}")
        
    items=trade_items_by_date(start_date,end_date)
    if items:
        create_batch("items",items)
    
    # => Leer los batches y comparar los atributos existentes
    # files = read_files("atributtesBatches")
    # process_files(files,connection)
    # move_files("atributtesBatches","itemsBatches")
                    
    # => Leer los batches para guardar en la BD
    
    # files=read_files("itemsBatches")
    

    