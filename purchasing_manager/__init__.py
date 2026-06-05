import os, sys, json

# pyrefly: ignore [missing-import]
from flask import Flask, url_for, redirect, current_app, session
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def create_app (test_config = None):
    """App factory"""
    app = Flask(__name__, instance_relative_config = True)
    CORS(app)

    _secret_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "client_secret.json")
    with open(_secret_path) as f:
        _google_creds = json.load(f)["web"]

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "change-me-in-production"),
        GOOGLE_CLIENT_ID=_google_creds["client_id"],
        GOOGLE_CLIENT_SECRET=_google_creds["client_secret"],
    )
    
    if test_config is None:
        # load the instance config file if it exists in instance folder (same level as this file)
        app.config.from_pyfile('config.py', silent=True)
    
    else:
         # load the test config if passed in
        app.config.from_mapping(test_config)
        
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.context_processor
    def inject_tenant_logo():
        return {"tenant_logo": session.get("tenant_logo")}
            
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
    
    from .routes import sample
    app.register_blueprint(sample.bp)

    from .routes import onboarding
    app.register_blueprint(onboarding.bp)

    from .routes import admin
    app.register_blueprint(admin.bp)
    
    
    @app.route("/")
    def home():
        return redirect("url_for('home.index')")
    
    uf_list = [{"uf":"AC", "name":"Acre"}, {"uf":"AL", "name":"Alagoas"}, {"uf":"AP", "name":"Amapá"}, {"uf":"AM", "name":"Amazonas"},
            {"uf":"BA", "name":"Bahia"}, {"uf":"CE", "name":"Ceará"}, {"uf":"DF", "name":"Distrito Federal"}, {"uf":"ES", "name":"Espírito Santo"},
            {"uf":"GO", "name":"Goiás"}, {"uf":"MA", "name":"Maranhão"}, {"uf":"MT", "name":"Mato Grosso"}, {"uf":"MS", "name":"Mato Grosso do Sul"},
            {"uf":"MG", "name":"Minas Gerais"}, {"uf":"PA", "name":"Pará"}, {"uf":"PB", "name":"Paraíba"}, {"uf":"PR", "name":"Paraná"},
            {"uf":"PE", "name":"Pernambuco"}, {"uf":"PI", "name":"Piauí"}, {"uf":"RJ", "name":"Rio de Janeiro"}, {"uf":"RN", "name":"Rio Grande do Norte"},
            {"uf":"RS", "name":"Rio Grande do Sul"}, {"uf":"RO", "name":"Rondônia"}, {"uf":"RR", "name":"Roraima"}, {"uf":"SC", "name":"Santa Catarina"},
            {"uf":"SP", "name":"São Paulo"}, {"uf":"SE", "name":"Sergipe"}, {"uf":"TO", "name":"Tocantins"}]

    with app.app_context():
        current_app.uf_list = uf_list
        
    return app

if __name__ == "__main__":
    
    sys.stdout.flush()
    
    app = create_app()