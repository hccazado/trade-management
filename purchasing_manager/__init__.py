import os

from flask import Flask, url_for, redirect

def create_app (test_config = None):
    """App factory"""
    app = Flask(__name__, instance_relative_config = True)
    
    app.config.from_mapping(
        SECRET_KEY='dev'
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

    @app.route("/")
    def home():
        return "Under development!"
    
    return app