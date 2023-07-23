from ..db import db


#Defining Clients Firebase collection
clients_ref = db.get_db().collection("clients")

def get_all():
    stream = clients_ref.get()

    client_structure = {}

    result = []

    for client in stream:
        
        client_structure = client
        
        client_structure["id"] = client.id
      
        result.append(client_structure)

    print(result)
    return result

