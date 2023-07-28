"""Script for reading files exported from mysql db as csv. then converting the models into json for future uploading to 
firebase database"""

import json

from purchasing_manager.models import client as model_client

with open("clientes.csv", "rt") as file:
    
    for line in file:
        
        line_list = line.strip("\n")
        line_list = line_list.split(";")
        
        #remove id from mysql
        line_list.pop(0)
        
        #remove last blank column (probably the \n field)
        #line_list.pop()
        #remove updated_at from sequelize
        line_list.pop(10)
        #remove created_at from sequelize
        #line_list.pop(11)
        
        
        
        
        #print(json.dumps(line_list, indent=4))
        
        #print(len(line_list))
        line_dictionary = {
            "nome": line_list[0][1:-1],
            "email": line_list[1][1:-1],
            "cnpj": line_list[2][1:-1],
            "ie": line_list[3][1:-1],
            "cep": line_list[4][1:-1],
            "end": line_list[5][1:-1],
            "num": line_list[6][1:-1],
            "bairro": line_list[7][1:-1],
            "cidade": line_list[8][1:-1],
            "uf": line_list[9][1:-1],
            "conta": line_list[12][1:-1]
        }
        
        #print(f"{json.dumps(line_dictionary, indent=4) }")
        
        if model_client.create(line_dictionary):
            print(f"Successfully added! warehouse: {line_dictionary['nome']}")
            
        else:
            print(f"ERROR!. NOT ADDED Warehouse: {line_dictionary['nome']}")
        
        
        