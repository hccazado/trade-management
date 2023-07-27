import flask, asyncio, json

from flask import Blueprint, url_for, request, session, redirect, render_template, flash, current_app

from ..models import client as model_client, warehouse as model_warehouse, agreement as model_agreement

from ..controllers import client as controller_client, warehouse as controller_warehouse, agreement as controller_agreement

def query_clients(query):

    if len(current_app.clients_collection) == 0:
        
        current_app.clients_collection = controller_client.update_clients_collection()

    function_name = lambda item: item["nome"]

    result = []

    for client in current_app.clients_collection:

        if query.upper() in  client["nome"].upper():

            result.append(client)

    if len(result) > 1:

        result = sorted(result, key=function_name())

        return result
    
    else:
    
        return result
    
def query_warehouses(query):

    if len(current_app.warehouses_collection) == 0:

        controller_warehouse.update_warehouses_collection()

    function_name = lambda item: item["nome"]

    result = []

    for warehouse in current_app.warehouses_collection:

        if query.upper() in warehouse["nome"].upper():

            result.append(warehouse)

    if len(result) > 1:

        result = sorted(result, key=function_name)

        return result
   
    else:
    
        return result
    
def query_agreements(query):

    if len(current_app.agreements_collection) == 0:

        controller_agreement.update_agreements_collection()

        current_app.clients_collection = model_client.get_all()

        current_app.warehouses_collection = model_warehouse.get_all()

    function_agreement = lambda item: item["num_fechamento"]

    result = []

    for agreement in current_app.agreements_collection:

        if query in agreement["num_fechamento"]:

            agreement['comprador'] = model_client.get_name(agreement['comprador'])
            agreement['vendedor'] = model_client.get_name(agreement['vendedor'])
            agreement['retirada'] = model_warehouse.get_name(agreement['retirada'])
            agreement['descarga'] = model_warehouse.get_name(agreement['descarga'])

            result.append(agreement)

    if len(result) > 1:

        result = sorted(result, key=function_agreement)

        return result
   
    else:
    
        return result