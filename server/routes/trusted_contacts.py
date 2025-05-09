from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.models import db, TrustedContact
from sqlalchemy.exc import SQLAlchemyError
import re
import phonenumbers

contacts_bp = Blueprint('contacts', __name__)

# Email validation
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone):
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False

# Create a new contact
@contacts_bp.route('/api/contacts', methods=['POST'])
@login_required
def create_contact():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        name = data.get('name')
        email= data.get('email')
        phone= data.get('phone')
        
        if not name or not email or not phone:
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_contact = TrustedContact(name=name, email=email, phone=phone, user_id=current_user.id)
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact created successfully',
            'contact': {
                'id': new_contact.id,
                'name': new_contact.name,
                'email': new_contact.email,
                'phone': new_contact.phone
            }
        }), 201
        
    except Exception as e:
        print("❌ Error in POST /api/contacts:", e)
        return jsonify({'error':"Server error"}),500

@contacts_bp.route('/api/contacts', methods=['GET'])
@login_required
def get_contacts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = TrustedContact.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)
    contacts = pagination.items

    return jsonify({
        'contacts': [{
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone
        } for contact in contacts],
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    }), 200


@contacts_bp.route('/api/contacts/<int:contact_id>', methods=['GET'])
@login_required
def get_contact(contact_id):
    contact = TrustedContact.query.filter_by(id=contact_id, user_id=current_user.id).first()
    
    if not contact:
        return jsonify({'error': 'Contact not found or access denied'}), 404
    
    return jsonify({
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'phone': contact.phone
    }), 200


@contacts_bp.route('/api/contacts/<int:contact_id>', methods=['PUT'])
@login_required
def update_contact(contact_id):
    contact = TrustedContact.query.filter_by(id=contact_id, user_id=current_user.id).first()
    
    if not contact:
        return jsonify({'error': 'Contact not found or access denied'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'name' in data:
            contact.name = data['name']
        
        if 'email' in data:
            if not is_valid_email(data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            contact.email = data['email']
        
        if 'phone' in data:
            if not is_valid_phone(data['phone']):
                return jsonify({'error': 'Invalid phone number format'}), 400
            contact.phone = data['phone']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Contact updated successfully',
            'contact': {
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone
            }
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@contacts_bp.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
@login_required
def delete_contact(contact_id):
    contact = TrustedContact.query.filter_by(id=contact_id, user_id=current_user.id).first()
    
    if not contact:
        return jsonify({'error': 'Contact not found or access denied'}), 404
    
    try:
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({'message': 'Contact deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@contacts_bp.route('/api/contacts/search', methods=['GET'])
@login_required
def search_contacts():
    query = request.args.get('query', '')
    if not query or len(query) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400
    
    search_query = f"%{query}%"
    contacts = TrustedContact.query.filter(
        TrustedContact.user_id == current_user.id,
        (TrustedContact.name.ilike(search_query) | TrustedContact.email.ilike(search_query))
    ).all()
    
    return jsonify({
        'contacts': [{
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone
        } for contact in contacts],
        'count': len(contacts)
    }), 200

@contacts_bp.route('/api/emergency/notify', methods=['POST'])
@login_required
def notify_emergency_contacts():
    data = request.get_json() or {}
    location = data.get('location')
    message = data.get('message', 'Emergency alert')
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    contacts = TrustedContact.query.filter_by(user_id=current_user.id).all()
    
    if not contacts:
        return jsonify({'error': 'No emergency contacts available'}), 404

    email_payload = {
        "contacts": [{
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone
        } for contact in contacts],
        "alert_details": {
            "user": current_user.username,
            "location": location,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    }
    
    return jsonify({
        "message": "Emergency notification data generated successfully",
        "email_payload": email_payload
    }), 200
