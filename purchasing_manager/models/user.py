from ..db import db

#Defining Users Firebase collection
users_ref = db.get_db().collection("users")

def get():
    
    users_stream = users_ref.get()
    
    user_struct = {}
    
    users = []

    for user in users_stream:
        
        user_struct = user.to_dict()
        
        user_struct["id"] = user.id
        
        users.append(user_struct)
             
    return users
    
def create(user_data):
    
    document = users_ref.document()
    
    if document.set(user_data):
        
        return True
    
    else:
        
        return False
    
    
    
    