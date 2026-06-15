from ..models import client as model_client, warehouse as model_warehouse, agreement as model_agreement, sample as model_sample, buyer as model_buyer


def query_clients(query):
    clients = model_client.get_all()
    result = [c for c in clients if query.upper() in c["nome"].upper()]
    return sorted(result, key=lambda c: c["nome"])

def query_warehouses(query):
    warehouses = model_warehouse.get_all()
    result = [w for w in warehouses if query.upper() in w["nome"].upper()]
    return sorted(result, key=lambda w: w["nome"])

def query_agreements(query):
    agreements = model_agreement.get_all()
    clients = {c['id']: c['nome'] for c in model_client.get_all()}
    warehouses = {w['id']: w['nome'] for w in model_warehouse.get_all()}
    result = []
    for agreement in agreements:
        if query in agreement["num_fechamento"]:
            agreement['comprador'] = clients.get(agreement.get('comprador', ''), '')
            agreement['vendedor'] = clients.get(agreement.get('vendedor', ''), '')
            agreement['retirada'] = warehouses.get(agreement.get('retirada', ''), '')
            agreement['descarga'] = warehouses.get(agreement.get('descarga', ''), '')
            result.append(agreement)
    return sorted(result, key=lambda a: a["num_fechamento"])

def query_samples(query):
    samples = model_sample.get_all()
    result = []
    for sample in samples:
        client_id = sample.get('client', '')
        client_name = model_client.get_name(client_id) if client_id else "Sem Cliente"
        if query.upper() in client_name.upper():
            sample['client_name'] = client_name
            result.append(sample)
    return sorted(result, key=lambda s: s.get('client_name', '').lower())

def query_buyers(query):
    buyers = model_buyer.get_all()
    result = [b for b in buyers if query.upper() in b.get("nome", "").upper()]
    return sorted(result, key=lambda b: b.get("nome", ""))
