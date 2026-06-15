from ..db.db import get_db


def get_all_tenants():
    tenants = []
    for doc in get_db().collection("tenants").get():
        tenant = doc.to_dict()
        tenant["id"] = doc.id
        tenants.append(tenant)
    return tenants


def get_tenant_users(tenant_id):
    users = []
    for doc in get_db().collection("users").where("tenant_id", "==", tenant_id).get():
        user = doc.to_dict()
        user["id"] = doc.id
        user.pop("password", None)
        users.append(user)
    return users
