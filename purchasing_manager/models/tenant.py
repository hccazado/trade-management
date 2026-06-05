import uuid
from ..db.db import get_db

def create(name):
    tenant_id = str(uuid.uuid4())
    get_db().collection("tenants").document(tenant_id).set({"name": name})
    return tenant_id

def get(tenant_id):
    doc = get_db().collection("tenants").document(tenant_id).get()
    if not doc.exists:
        return None
    return {"id": doc.id, **doc.to_dict()}

def update(tenant_id, data):
    get_db().collection("tenants").document(tenant_id).update(data)
