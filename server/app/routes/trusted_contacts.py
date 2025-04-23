from flask import Blueprint, request, jsonify
from ..models import db, TrustedContact
from flask_jwt_extended import jwt_required, get_jwt_identity

trusted_contact_bp = Blueprint('..trusted_contacts', __name__, url_prefix="/contacts")

@trusted_contact_bp.route("/", methods=["POST"])
@jwt_required()
def add_contact():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    new_contact = TrustedContact(
        name=data["name"],
        phone=data.get("phone"),
        email=data.get("email"),
        user_id=user_id
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({"message": "Contact added successfully"}), 201

@trusted_contact_bp.route("/", methods=["GET"])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()
    contacts = TrustedContact.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "phone": c.phone,
        "email": c.email
    } for c in contacts]), 200
