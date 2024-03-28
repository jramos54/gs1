import requests
import os, datetime, time
from dataprocessing import date_conversion
from dotenv import load_dotenv
load_dotenv()
# import logging
# logging.basicConfig(level=logging.INFO)

def trade_items_by_gpc(gpc,start_date,end_date):
   
    url = "https://apisync.syncfonia.com/wsproxy/apiServices/tradeItemService.svc/Search"
    page_number = 1
    page_size = 100
    total_elements = []
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    # print(username,password)
    headers = {
        "Content-Type": "application/json",
    }

    while True:
        payload = {
            "LastChangedEndDateTime": date_conversion(end_date),
            "LastChangedStartDateTime": date_conversion(start_date),
            "TargetMarketCountryCode": "484",
            "Gpc": gpc,
            "PageNumber": page_number,
            "PageSize": page_size,
            "TradeItemModules": ["ALL"]
        }
        try:
            response = requests.post(url, json=payload, headers=headers, auth=(username, password))            
            time.sleep(30)

            if response.status_code == 200:
                data = response.json()
                if data.get("Errors") is None:
                    trade_item_list = data.get('TradeItemList', [])
                    print(f"total elements : {len(trade_item_list)}")
                    total_elements.extend(trade_item_list)
                    page_number += 1
                    if len(trade_item_list)<page_size:
                        print(f"La paginación ha finalizado. La ultima extraccion fue {len(trade_item_list)}")
                        break
                    
                else:
                    print(f"La paginación ha finalizado.\n{data.get('Errors')}")
                    break
            else:
                print(f"Error al consumir la API. Código de estado: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a la API: {e}")
            # logging.exception("Error al conectarse a la API")
            break

    return total_elements


def trade_items_by_date(start_date,end_date):
   
    url = "https://apisync.syncfonia.com/wsproxy/apiServices/tradeItemService.svc/Search"
    page_number = 1
    page_size = 100
    total_elements = []
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    print(username,password)
    headers = {
        "Content-Type": "application/json",
    }

    while True:
        payload = {
            "LastChangedEndDateTime": date_conversion(end_date),
            "LastChangedStartDateTime": date_conversion(start_date),
            "TargetMarketCountryCode": "484",
            "PageNumber": page_number,
            "PageSize": page_size,
            "TradeItemModules": ["ALL"]
        }
        # print(payload)
        try:
            time.sleep(60)
            response = requests.post(url, json=payload, headers=headers, auth=(username, password))
            # print(response.text)
            data = response.json()
            if response.status_code == 200:
                if data.get("Errors") is None:
                    trade_item_list = data.get('TradeItemList', [])
                    print(f"total elements : {len(trade_item_list)}")
                    total_elements.extend(trade_item_list)
                    page_number += 1
                else:
                    print("x"*50)
                    print(f"La paginación ha finalizado.\n{data.get('Errors')}")
                    break
            else:
                print(f"Error al consumir la API. Código de estado: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a la API: {e}")
            # logging.exception("Error al conectarse a la API")
            break

    return total_elements


def trade_items_by_gnl(gnl):
   
    url = "https://apisync.syncfonia.com/wsproxy/apiServices/tradeItemService.svc/Search"
    page_number = 1
    page_size = 100
    total_elements = []
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    # print(username,password)
    headers = {
        "Content-Type": "application/json",
    }

    while True:
        payload = {
            "TradeItemKey": {
                "Gln": gnl,
                "TargetMarketCountryCode": "484"
            },
        
            "PageNumber": page_number,
            "PageSize": page_size,
            "TradeItemModules": [
                "ALL"
            ]
        }
        # print(payload)
        try:
            response = requests.post(url, json=payload, headers=headers, auth=(username, password))
            # print(response.text)
            data = response.json()
            if response.status_code == 200:
                if data.get("Errors") is None:
                    trade_item_list = data.get('TradeItemList', [])
                    print(f"total elements : {len(trade_item_list)}")
                    total_elements.extend(trade_item_list)
                    page_number += 1
                else:
                    print("x"*50)
                    print(f"La paginación ha finalizado.\n{data.get('Errors')}")
                    break
            else:
                print(f"Error al consumir la API. Código de estado: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a la API: {e}")
            # logging.exception("Error al conectarse a la API")
            break

    return total_elements


def trade_items_by_gnl(gnl):
   
    url = "https://apisync.syncfonia.com/wsproxy/apiServices/tradeItemService.svc/Search"
    page_number = 1
    page_size = 100
    total_elements = []
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    # print(username,password)
    headers = {
        "Content-Type": "application/json",
    }

    while True:
        payload = {
            "TradeItemKey": {
                "Gln": gnl,
                "TargetMarketCountryCode": "484"
            },
        
            "PageNumber": page_number,
            "PageSize": page_size,
            "TradeItemModules": [
                "ALL"
            ]
        }
        # print(payload)
        try:
            response = requests.post(url, json=payload, headers=headers, auth=(username, password))
            # print(response.text)
            data = response.json()
            if response.status_code == 200:
                if data.get("Errors") is None:
                    trade_item_list = data.get('TradeItemList', [])
                    print(f"total elements : {len(trade_item_list)}")
                    total_elements.extend(trade_item_list)
                    page_number += 1
                else:
                    print("x"*50)
                    print(f"La paginación ha finalizado.\n{data.get('Errors')}")
                    break
            else:
                print(f"Error al consumir la API. Código de estado: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a la API: {e}")
            # logging.exception("Error al conectarse a la API")
            break

    return total_elements

# if __name__=="__main__":
#     start_date="2017-01-01"
#     today=datetime.datetime.today()
#     end_date=today.strftime("%Y-%m-%d")
    
#     items=trade_items_by_gpc("10001961",start_date,end_date)
    
#     print(items)