from flask import Flask
from flask_login import LoginManager
from config import Config
from models.models import db, User
from routes.auth import auth_bp
from views import views_bp
from routes.trip import trip_bp
from routes.journal_entries import journal_bp
from routes.trusted_contacts import contacts_bp
from routes.locations import locations_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(trip_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(locations_bp)
    
    # Create database tables before first request
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)