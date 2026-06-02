"""
Migrate top-level Firestore collections into tenant subcollections.

  tenants/cazadocafe/clients/
  tenants/cazadocafe/warehouses/
  tenants/cazadocafe/agreements/
  tenants/cazadocafe/samples/

Users stay in the top-level `users` collection but get a `tenant_id` field added.

This script ONLY copies/updates — it never deletes. After you verify everything
looks correct in Firestore, delete the old top-level collections manually.

Run from the project root:
    venv/bin/python data_migration_scripts/migrate_to_tenants.py
"""

import uuid
import firebase_admin
from firebase_admin import credentials, firestore

TENANT_ID = str(uuid.uuid4())
TENANT_USERNAME = "cazadocafe"
BUSINESS_COLLECTIONS = ["clients", "warehouses", "agreements", "samples"]

CREDENTIAL = credentials.Certificate("./prc-mgt.json")
firebase_admin.initialize_app(CREDENTIAL)
db = firestore.client()

tenant_ref = db.collection("tenants").document(TENANT_ID)
tenant_ref.set({"name": "Caza do Café", "username": TENANT_USERNAME})
print(f"Tenant document created: tenants/{TENANT_ID} (username: {TENANT_USERNAME})")

for collection_name in BUSINESS_COLLECTIONS:
    docs = db.collection(collection_name).get()
    count = 0
    for doc in docs:
        tenant_ref.collection(collection_name).document(doc.id).set(doc.to_dict())
        count += 1
    print(f"  {collection_name}: {count} documents copied → tenants/{TENANT_ID}/{collection_name}/")

users = db.collection("users").get()
count = 0
for user in users:
    db.collection("users").document(user.id).update({"tenant_id": TENANT_ID})
    count += 1
print(f"  users: {count} documents updated with tenant_id='{TENANT_ID}'")

print("\nMigration complete. Verify the data in Firestore before deleting the old collections.")
