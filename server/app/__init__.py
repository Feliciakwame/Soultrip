from flask import Flask
from .extensions import db, migrate,jwt,mail

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY']='your-secret-key'
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=587
    app.config['MAIL_USE_TLS']=True
    app.config['MAIL_USERNAME']='your_email@gmail.com'
    app.config['MAIL_PASSWORD']='your_email_password'
    mail.init_app(app)
    

    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from .routes import api_blueprints
    for bp in api_blueprints:
        app.register_blueprint(bp)

    
    from .routes.journal_routes import journal_bp
    app.register_blueprint(journal_bp)
    
    from .routes.trusted_contacts import trusted_contacts_bp
    
    app.register_blueprint(trusted_contacts_bp, url_prefix='/trusted-contacts')
    
    print("Registered routes:",[rule.rule for rule in app.url_map.iter_rules()])
    
    return app