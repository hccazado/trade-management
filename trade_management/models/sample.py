from firebase_admin import exceptions
from ..db.db import tenant_col

def _ref():
    return tenant_col("samples")

def create(new_data):
    try:
        _ref().document().set(new_data)
        return True
    except exceptions.FirebaseError as fire_error:
        print(fire_error.http_response, fire_error.cause)
        return False

def get_all():
    samples = []
    for doc in _ref().get():
        sample = doc.to_dict()
        sample["id"] = doc.id
        samples.append(sample)
    return samples

def get_one(id=None):
    if not id:
        return {}
    doc = _ref().document(id).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return {}

def update(id, new_data):
    try:
        _ref().document(id).set(new_data)
        return True
    except exceptions.FirebaseError as fire_error:
        print(fire_error.http_response, fire_error.cause)
        return False
