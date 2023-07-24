from ..db import db


#Defining Clients Firebase collection
clients_ref = db.get_db().collection("clients")

def get_all():
     
    stream = clients_ref.get()
    
    client_structure = {}
    
    clients = []
    
    for client in stream:
        
        client_structure = client.to_dict()
        
        client_structure["id"] = client.id
      
        clients.append(client_structure)

    return clients

def get_name(key):
    client = clients_ref.document(key).get()

    client_struct = client.to_dict()

    return client_struct['nome']

