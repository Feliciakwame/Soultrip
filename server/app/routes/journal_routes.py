from flask import Blueprint,request,jsonify
from app.models import db,JournalEntry

journal_bp=Blueprint('journal_bp',__name__)

@journal_bp.route('/journal_entries',methods=['GET'])
def get_entries():
    entries = JournalEntry.query.all()
    return jsonify([entry.to_dict() for entry in entries]),200


    
@journal_bp.route('/journal_entries', methods=['POST'])
def create_entry():
    data = request.get_json()
    new_entry = JournalEntry(
        title=data['title'],
        content=data['content'],
        trip_id=data['trip_id']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()),201