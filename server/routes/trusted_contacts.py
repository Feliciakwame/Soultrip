from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.models import db, TrustedContact
from sqlalchemy.exc import SQLAlchemyError
import re

contacts_bp = Blueprint('contacts', __name__)

# Helper function to validate email format
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# Helper function to validate phone format
def is_valid_phone(phone):
    # Accept digits, spaces, dashes, parentheses, and plus sign
    pattern = r'^[0-9\s\-\(\)\+]+$'
    return bool(re.match(pattern, phone)) and len(re.sub(r'[^\d]', '', phone)) >= 7

# ----- TRUSTED CONTACTS ROUTES -----

@contacts_bp.route('/api/contacts', methods=['POST'])
@login_required
def create_contact():
    data = request.get_json()
    
    # Validate request data
    if not data or not all(k in data for k in ('name', 'email', 'phone')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate phone number
    if not is_valid_phone(data['phone']):
        return jsonify({'error': 'Invalid phone number format'}), 400
    
    try:
        # Create trusted contact
        contact = TrustedContact(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            user_id=current_user.id
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact added successfully',
            'contact': {
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone
            }
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@contacts_bp.route('/api/contacts', methods=['GET'])
@login_required
def get_contacts():
    contacts = TrustedContact.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'contacts': [{
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone
        } for contact in contacts]
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
        # Update fields if provided
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
    """Search contacts by name or email"""
    
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
    """
    Endpoint to notify emergency contacts.
    Returns data needed for EmailJS in the frontend.
    """
    data = request.get_json() or {}
    location = data.get('location', 'Unknown location')
    message = data.get('message', 'Emergency alert')
    
    # Get all trusted contacts for the current user
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