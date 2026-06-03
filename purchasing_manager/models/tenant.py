import uuid
from ..db.db import get_db

def create(name):
    """Creates a new tenant document with a UUID key. Returns the tenant ID."""
    tenant_id = str(uuid.uuid4())
    get_db().collection("tenants").document(tenant_id).set({"name": name})
    return tenant_id

def update(tenant_id, data):
    get_db().collection("tenants").document(tenant_id).update(data)
