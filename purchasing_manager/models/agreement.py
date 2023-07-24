from firebase_admin import exceptions

from ..db import db

agreement_ref = db.get_db().collection("agreements")

def get_all():

    agreements_stream = agreement_ref.get()

    agreement_struct = {}

    agreements = []

    for agreement in agreements_stream:
        agreement_struct = agreement.to_dict()

        agreement_struct["id"] = agreement.id

        agreements.append(agreement_struct)

    return agreements

def create(new_agreement):

    doc = agreement_ref.document()

    try:
        doc.set(new_agreement)

        return True
            
    except exceptions.FirebaseError as fire_error:
            
        print(fire_error.http_response, fire_error.cause)
            
        return False

