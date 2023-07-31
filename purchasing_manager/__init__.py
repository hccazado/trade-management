import os, requests, sys

from flask import Flask, url_for, redirect, current_app
from flask_cors import CORS


def create_app (test_config = None):
    """App factory"""
    app = Flask(__name__, instance_relative_config = True)
    CORS(app)
    
    app.config.from_mapping(
        SECRET_KEY= os.urandom(24)
        #SECRET_KEY= "DEV"
    )
    
    if test_config is None:
        # load the instance config file if it exists in instance folder (same level as this file)
        app.config.from_pyfile('config.py', silent=True)
    
    else:
         # load the test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
            
    #defining a static starting page while developing app
    @app.route("/favicon.ico")
    def favicon():
        return redirect(url_for("static", filename = "favicon.ico"))
    
    from .routes import home
    app.register_blueprint(home.bp)
    
    from .routes import warehouse
    app.register_blueprint(warehouse.bp)
    
    from .routes import agreement
    app.register_blueprint(agreement.bp)
    
    from .routes import client
    app.register_blueprint(client.bp)
    
    from .routes import auth
    app.register_blueprint(auth.bp)

    from .routes import api
    app.register_blueprint(api.bp)
    
    
    @app.route("/")
    def home():
        return redirect("url_for('home.index')")
    
    #context variables (for avoiding firebase recursive  calling)
    clients_collection = []
    warehouses_collection = []
    agreements_collection = []
    
    uf_list = [{"uf":"AC", "name":"Acre"}, {"uf":"AL", "name":"Alagoas"}, {"uf":"AP", "name":"Amapá"}, {"uf":"AM", "name":"Amazonas"},
            {"uf":"BA", "name":"Bahia"}, {"uf":"CE", "name":"Ceará"}, {"uf":"DF", "name":"Distrito Federal"}, {"uf":"ES", "name":"Espírito Santo"},
            {"uf":"GO", "name":"Goiás"}, {"uf":"MA", "name":"Maranhão"}, {"uf":"MT", "name":"Mato Grosso"}, {"uf":"MS", "name":"Mato Grosso do Sul"},
            {"uf":"MG", "name":"Minas Gerais"}, {"uf":"PA", "name":"Pará"}, {"uf":"PB", "name":"Paraíba"}, {"uf":"PR", "name":"Paraná"},
            {"uf":"PE", "name":"Pernambuco"}, {"uf":"PI", "name":"Piauí"}, {"uf":"RJ", "name":"Rio de Janeiro"}, {"uf":"RN", "name":"Rio Grande do Norte"},
            {"uf":"RS", "name":"Rio Grande do Sul"}, {"uf":"RO", "name":"Rondônia"}, {"uf":"RR", "name":"Roraima"}, {"uf":"SC", "name":"Santa Catarina"},
            {"uf":"SP", "name":"São Paulo"}, {"uf":"SE", "name":"Sergipe"}, {"uf":"TO", "name":"Tocantins"}]
    
    with app.app_context():
        current_app.clients_collection = clients_collection
        current_app.warehouses_collection = warehouses_collection
        current_app.agreements_collection = agreements_collection
        current_app.uf_list = uf_list
        
    return app

if __name__ == "__main__":
    
    sys.stdout.flush()
    
    app = create_app()