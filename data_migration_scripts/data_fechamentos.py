"""Script for reading files exported from mysql db as csv. then converting the models into json for future uploading to 
firebase database"""

import json

from datetime import datetime

from purchasing_manager.models import warehouse as model_warehouse, client as model_client, agreement as model_agreement


clients = model_client.get_all()
warehouses = model_warehouse.get_all()

def get_id_client(name):
    for client in clients:
        
        if client["nome"].upper() in name.upper():
            return client["id"]
        
def get_id_warehouse(name):
    for warehouse in warehouses:
        
        if warehouse["nome"].upper() in name.upper():
            return warehouse["id"]
        
def get_account_client(id):
    for client in clients:
        
        if client["id"] == id:
            return client["conta"]
        
def adjust_date(date):
    
    new_date = date[2:4]+"/"+date[5:7]+"/"+date[8:10]
    
    split_date = new_date.split("/")
    
    new_date = split_date[2]+"/"+split_date[1]+"/"+split_date[0]
    
    return new_date

def agreements_current_year(agreement):
    """returns only dictionaries from current year"""
    
    current_yr = datetime.now().strftime("%y")
    
    split_dt = agreement["data"].split("/")
    
    agreement_yr = split_dt[2]
    
    if agreement_yr == current_yr:
        
        return agreement
    
def order_agreements_number(agreements):
    
    #function_number = lambda item: item["num_fechamento"][0:3]+item["num_fechamento"][4:6]
    function_number = lambda item: item["num_fechamento"][0:3]
    
    function_year_22 = lambda item: item["num_fechamento"][4:6] == '22'
    
    agreements_22 = list(filter(function_year_22, agreements))
    
    function_year_23 = lambda item: item["num_fechamento"][4:6] == '23'

    agreements_23 = list(filter(function_year_23, agreements))
    
    agreements_23 = sorted(agreements_23, key = function_number)
    
    ordered_lists = agreements_22 + agreements_23
    
    
    #print(json.dumps(ordered_lists, indent=3))
    
    return ordered_lists

agreements = []

with open("fechamentos2.csv", "rt") as file:
    count =0
    for line in file:
        line_list = line.strip("\n")
        line_list = line_list.split(";")
        
        if not len(line_list) < 15:
        
            line_dictionary = {
                "created_at": datetime.now().strftime("%d/%m/%y - %H:%M"),
                "num_fechamento": line_list[0][0:4]+line_list[0][6:8],
                "comprador": line_list[1],
                "vendedor": line_list[2],
                "rc": line_list[3],
                "data": line_list[4],
                "retirada": line_list[5],
                "descarga": line_list[6],
                "cond_venda": line_list[7],
                "preco": line_list[8],
                "quantidade": line_list[9],
                "modalidade": line_list[10],
                "pagamento": line_list[12],
                "corretor": line_list[13],
                "corretagem_vendedor": line_list[14],
                "corretagem_comprador": line_list[15],
                "obs": line_list[16],
            }
        
            agreements.append(line_dictionary)
            

for agreement in agreements:
    
    agreement["data"] = adjust_date(agreement["data"])
    
    agreement["vendedor"] = get_id_client(agreement["vendedor"])
    
    if agreement["pagamento"] is None:
        
        agreement["pagamento"] = get_account_client(agreement["vendedor"])
    
    agreement["comprador"] = get_id_client(agreement["comprador"])
    
    agreement["retirada"] = get_id_warehouse(agreement["retirada"])
    
    agreement["descarga"] = get_id_warehouse(agreement["descarga"])
    
    #print(json.dumps(agreement, indent=4))

agreements = order_agreements_number(agreements)

for idx, agreement in enumerate(agreements):
    
    #print(json.dumps(agreement["data"], indent=2))
    agreement["index"] = idx+1
    #if model_agreements.update(agreement["id"],agreement):
       #print(f"Successfully updated! Agreement: {agreement['num_fechamento']}")
   # else:
        #print(f"Something went wrong! Agreement: {agreement['num_fechamento']}")
    #print(json.dumps(agreement, indent=4))
    

        
#print(json.dumps(order_agreements_number(agreements), indent=4))

for agreement in agreements:
    
    print(json.dumps(agreement["index"], indent=4))
    
    #if model_agreement.create(agreement):
        
    #    print(f"Successfully added! Agreement: {agreement['num_fechamento']} Index: {agreement['index']}")
        
    #else: 
        
    #    print(f"ERROR Adding Agreement. Agreement{agreement['num_fechamento']} Index: {agreement['index']}")