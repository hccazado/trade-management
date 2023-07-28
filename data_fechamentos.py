"""Script for reading files exported from mysql db as csv. then converting the models into json for future uploading to 
firebase database"""

import json

from purchasing_manager.models import warehouse as model_warehouse, client as model_client, agreement as model_agreement


clients = model_client.get_all()
warehouses = model_warehouse.get_all()

def get_id_client(name):
    for client in clients:
        
        if client["nome"].upper() == name.upper():
            return client["id"]
        
def get_id_warehouse(name):
    for warehouse in warehouses:
        
        if warehouse["nome"].upper() == name.upper():
            return warehouse["id"]
        
def get_account_client(id):
    for client in clients:
        
        if client["id"] == id:
            return client["conta"]

agreements = []

with open("fechamentos2.csv", "rt") as file:
    count =0
    for line in file:
        line_list = line.strip("\n")
        line_list = line_list.split(";")
        
        #remove id from mysql
        #line_list.pop(0)
        
        #remove last blank column (probably the \n field)
        #line_list.pop()
        #remove updated_at from sequelize
        #line_list.pop()
        #remove created_at from sequelize
        #line_list.pop()
                
        
        #if len(line_list) < 17 and not len(line_list) == 0:
        #print(json.dumps(line_list, indent=4))
        if not len(line_list) < 15:
        
            line_dictionary = {
                "num_fechamento": line_list[0],
                "vendedor": line_list[1],
                "comprador": line_list[2],
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
    agreement["vendedor"] = get_id_client(agreement["vendedor"])
    agreement["pagamento"] = get_account_client(agreement["vendedor"])
    agreement["comprador"] = get_id_client(agreement["comprador"])
    agreement["retirada"] = get_id_client(agreement["retirada"])
    agreement["descarga"] = get_id_client(agreement["descarga"])
    
for agreement in agreements:
    #print(json.dumps(agreement, indent=4))
    if model_agreement.create(agreement):
        
        print(f"Successfully added! warehouse: {agreement['num_fechamento']}")
        
    else: 
        
        print(f"ERROR Adding Agreement. Agreement{agreement['num_fechamento']}")
           
        