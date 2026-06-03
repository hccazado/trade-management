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


def get_by_email(email):
    results = users_ref.where("email", "==", email).limit(1).get()
    for doc in results:
        user = doc.to_dict()
        user["id"] = doc.id
        return user
    return None


def get_or_create_google_user(google_info):
    user = get_by_email(google_info["email"])
    if user:
        return user
    from . import tenant as model_tenant
    tenant_id = model_tenant.create(google_info.get("name", google_info["email"]))
    name = google_info.get("name", google_info["email"])
    doc = users_ref.document()
    doc.set({
        "name": name,
        "email": google_info["email"],
        "google_id": google_info["sub"],
        "tenant_id": tenant_id,
        "onboarding": True,
    })
    return {"id": doc.id, "name": name, "email": google_info["email"], "tenant_id": tenant_id, "onboarding": True}


def complete_onboarding(user_id):
    users_ref.document(user_id).update({"onboarding": False})

def reset_password(user_id, new_password):
    from werkzeug.security import generate_password_hash
    users_ref.document(user_id).update({"password": generate_password_hash(new_password)})
    
    
    
    