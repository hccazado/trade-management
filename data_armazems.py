"""Script for reading files exported from mysql db as csv. then converting the models into json for future uploading to 
firebase database"""

import json

from purchasing_manager.models import warehouse as model_warehouse

with open("armazems.csv", "rt") as file:
    
    for line in file:
        
        line_list = line.strip("\n")
        line_list = line_list.split(";")
        
        #remove id from mysql
        line_list.pop(0)
        
        #remove last blank column (probably the \n field)
        line_list.pop()
        #remove updated_at from sequelize
        line_list.pop()
        #remove created_at from sequelize
        line_list.pop()
          
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
            "uf": line_list[9][1:-1]
        }
        
        if model_warehouse.create(line_dictionary):
            print(f"Successfully added! warehouse: {line_dictionary['nome']}")
            
        else:
            print(f"ERROR!. NOT ADDED Warehouse: {line_dictionary['nome']}")
        
        #print(f"{json.dumps(line_dictionary, indent=4) }")
        
        
        