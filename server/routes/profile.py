from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User

profile_bp = Blueprint("profile_bp", __name__, url_prefix="/api")

@profile_bp.route("/api/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        
    })

@profile_bp.route("/api/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    
    db.session.commit()
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        
    })
