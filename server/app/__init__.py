from flask import Flask
from .extensions import db, migrate,jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY']='your-secret-key'
    

    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from .routes import api
    app.register_blueprint(api,url_prefix='/api')
    
    from .routes.journal_routes import journal_bp
    app.register_blueprint(journal_bp)
    
    print("Registered routes:",[rule.rule for rule in app.url_map.iter_rules()])
    
    return app