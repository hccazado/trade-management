"""
Backup all Firestore collections to a local JSON file.
Run from the project root:  python data_migration_scripts/backup_firestore.py
"""

import json
import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

CREDENTIAL = credentials.Certificate("./prc-mgt.json")
firebase_admin.initialize_app(CREDENTIAL)
db = firestore.client()

COLLECTIONS = ["users", "clients", "warehouses", "agreements", "samples"]

backup = {}

for collection_name in COLLECTIONS:
    docs = db.collection(collection_name).get()
    backup[collection_name] = {}
    for doc in docs:
        backup[collection_name][doc.id] = doc.to_dict()
    print(f"  {collection_name}: {len(backup[collection_name])} documents")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data_migration_scripts/backup_{timestamp}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(backup, f, ensure_ascii=False, indent=2, default=str)

print(f"\nBackup saved to {filename}")
