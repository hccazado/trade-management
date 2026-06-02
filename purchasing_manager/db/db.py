import firebase_admin
from firebase_admin import credentials, firestore, exceptions
import requests, os

#Initialize Firebase Firestore connection
CREDENTIAL = credentials.Certificate("./prc-mgt.json")

app = firebase_admin.initialize_app(CREDENTIAL)

db = firestore.client()

def get_db():
    """Returns Firebase client connection to interact with Firestore"""
    return db

def tenant_col(collection_name):
    """Returns a Firestore collection reference scoped to the current request's tenant."""
    from flask import g
    return db.collection("tenants").document(g.tenant_id).collection(collection_name)
