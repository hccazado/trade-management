from firebase_admin import exceptions
from ..db.db import tenant_col

def _ref():
    return tenant_col("agreements")

def get_all():
    agreements = []
    for doc in _ref().get():
        agreement = doc.to_dict()
        agreement["id"] = doc.id
        agreements.append(agreement)
    return agreements

def get_one(id=None):
    if not id:
        return {}
    doc = _ref().document(id).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return {}

def create(new_agreement):
    try:
        _ref().document().set(new_agreement)
        return True
    except exceptions.FirebaseError as fire_error:
        print(fire_error.http_response, fire_error.cause)
        return False

def update(id, new_data):
    try:
        _ref().document(id).set(new_data)
        return True
    except exceptions.FirebaseError as fire_error:
        print(fire_error.http_response, fire_error.cause)
        return False
