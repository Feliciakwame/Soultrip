from flask import Blueprint, jsonify, request
from app.models import db, User

profile_routes = Blueprint('profile_routes', __name__)


@profile_routes.route('/profile', methods=['GET'])
def get_profile():
    user = User.query.first() 
    if user:
        return jsonify(user.to_dict())
    return jsonify({'error': 'User not found'}), 404

@profile_routes.route('/profile', methods=['PATCH'])
def update_profile():
    data = request.get_json()
    user = User.query.first()  
    
    if user:
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify(user.to_dict())
    return jsonify({'error': 'User not found'}), 404
