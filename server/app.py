from flask import Flask
from flask import jsonify
from flask_login import login_required
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
from models.models import db, User
from routes.auth import auth_bp
from views import views_bp
from routes.trip import trip_bp
from routes.journal_entries import journal_bp
from routes.trusted_contacts import contacts_bp
from routes.locations import locations_bp
from routes.profile import profile_bp


def create_app():
    app = Flask(__name__)
    CORS(app)  
    app.config.from_object(Config)
    
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': 'Unauthorized access'}), 401
    
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(trip_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(profile_bp)
    
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)