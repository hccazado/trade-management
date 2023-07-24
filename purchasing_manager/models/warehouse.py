from ..db import db

warehouses_ref = db.get_db().collection("warehouses")

def get_all():
    stream = warehouses_ref.get()
    
    warehouse_structure = {}
    
    warehouses = []
    
    for warehouse in stream:
        
        warehouse_structure = warehouse.to_dict()
        
        warehouse_structure["id"] = warehouse.id
      
        warehouses.append(warehouse_structure)

    return warehouses

def get_name(key):

    warehouse = warehouses_ref.document(key).get()

    warehouse_struct = warehouse.to_dict()

    return warehouse_struct['nome']

