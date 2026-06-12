import firebase_admin
from firebase_admin import credentials, firestore, exceptions
import requests, os, json

_cred_json = os.environ.get("FIREBASE_CREDENTIALS")
if _cred_json:
    CREDENTIAL = credentials.Certificate(json.loads(_cred_json))
else:
    _cert_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prc-mgt.json")
    CREDENTIAL = credentials.Certificate(_cert_path)

app = firebase_admin.initialize_app(CREDENTIAL)

db = firestore.client()

def get_db():
    """Returns Firebase client connection to interact with Firestore"""
    return db

def tenant_col(collection_name):
    """Returns a Firestore collection reference scoped to the current request's tenant."""
    from flask import g
    return db.collection("tenants").document(g.tenant_id).collection(collection_name)
