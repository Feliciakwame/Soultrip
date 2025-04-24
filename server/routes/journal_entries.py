from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.models import db, JournalEntry
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

journal_bp = Blueprint('journal', __name__)

# ----- JOURNAL ENTRY ROUTES -----

@journal_bp.route('/api/journal', methods=['POST'])
@login_required
def create_journal_entry():
    data = request.get_json()
    
    # Validate request data
    if not data or not all(k in data for k in ('title', 'content')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Create journal entry
        entry = JournalEntry(
            title=data['title'],
            content=data['content'],
            user_id=current_user.id
        )
        
        db.session.add(entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Journal entry created successfully',
            'journal_entry': entry.to_dict()
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@journal_bp.route('/api/journal', methods=['GET'])
@login_required
def get_journal_entries():
    # Optional query parameters for filtering
    limit = request.args.get('limit', type=int)
    
    query = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.created_at.desc())
    
    if limit:
        query = query.limit(limit)
    
    entries = query.all()
    
    return jsonify({
        'journal_entries': [entry.to_dict() for entry in entries],
        'count': len(entries)
    }), 200

@journal_bp.route('/api/journal/<int:entry_id>', methods=['GET'])
@login_required
def get_journal_entry(entry_id):
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    
    if not entry:
        return jsonify({'error': 'Journal entry not found or access denied'}), 404
    
    return jsonify(entry.to_dict()), 200

@journal_bp.route('/api/journal/<int:entry_id>', methods=['PUT'])
@login_required
def update_journal_entry(entry_id):
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    
    if not entry:
        return jsonify({'error': 'Journal entry not found or access denied'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update fields if provided
        if 'title' in data:
            entry.title = data['title']
        
        if 'content' in data:
            entry.content = data['content']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Journal entry updated successfully',
            'journal_entry': entry.to_dict()
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@journal_bp.route('/api/journal/<int:entry_id>', methods=['DELETE'])
@login_required
def delete_journal_entry(entry_id):
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    
    if not entry:
        return jsonify({'error': 'Journal entry not found or access denied'}), 404
    
    try:
        db.session.delete(entry)
        db.session.commit()
        
        return jsonify({'message': 'Journal entry deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@journal_bp.route('/api/journal/search', methods=['GET'])
@login_required
def search_journal_entries():
    """Search journal entries by keywords in title or content"""
    
    query = request.args.get('query', '')
    if not query or len(query) < 3:
        return jsonify({'error': 'Search query must be at least 3 characters'}), 400
    
    # Search in both title and content
    search_query = f"%{query}%"
    entries = JournalEntry.query.filter(
        JournalEntry.user_id == current_user.id,
        (JournalEntry.title.ilike(search_query) | JournalEntry.content.ilike(search_query))
    ).order_by(JournalEntry.created_at.desc()).all()
    
    return jsonify({
        'journal_entries': [entry.to_dict() for entry in entries],
        'count': len(entries),
        'query': query
    }), 200

@journal_bp.route('/api/journal/stats', methods=['GET'])
@login_required
def get_journal_stats():
    """Get statistics about the user's journal entries"""
    
    # Total count of entries
    entry_count = JournalEntry.query.filter_by(user_id=current_user.id).count()
    
    # Get the date of the first entry
    first_entry = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.created_at).first()
    first_entry_date = first_entry.created_at if first_entry else None
    
    # Get the date of the most recent entry
    latest_entry = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.created_at.desc()).first()
    latest_entry_date = latest_entry.created_at if latest_entry else None
    
    # Average content length
    if entry_count > 0:
        avg_length_query = db.session.query(db.func.avg(db.func.length(JournalEntry.content))).filter(
            JournalEntry.user_id == current_user.id
        ).scalar()
        avg_content_length = int(avg_length_query) if avg_length_query else 0
    else:
        avg_content_length = 0
    
    return jsonify({
        'total_entries': entry_count,
        'first_entry_date': first_entry_date.strftime('%Y-%m-%d') if first_entry_date else None,
        'latest_entry_date': latest_entry_date.strftime('%Y-%m-%d') if latest_entry_date else None,
        'avg_content_length': avg_content_length
    }), 200