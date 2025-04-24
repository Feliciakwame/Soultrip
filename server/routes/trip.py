from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.models import db, Trip, Location
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

trip_bp = Blueprint('trip', __name__)

# ----- TRIP ROUTES -----

@trip_bp.route('/api/trips', methods=['POST'])
@login_required
def create_trip():
    data = request.get_json()
    
    # Validate request data
    if not data or not all(k in data for k in ('destination', 'start_date', 'end_date')):
        return jsonify({'error': 'Missing required trip fields'}), 400
    
    try:
        # Parse dates
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        # Validate dates
        if end_date < start_date:
            return jsonify({'error': 'End date cannot be before start date'}), 400
        
        # Create trip
        trip = Trip(
            destination=data['destination'],
            start_date=start_date,
            end_date=end_date,
            user_id=current_user.id
        )
        
        db.session.add(trip)
        db.session.commit()
        
        return jsonify({
            'message': 'Trip created successfully',
            'trip_id': trip.id,
            'destination': trip.destination,
            'start_date': trip.start_date.isoformat(),
            'end_date': trip.end_date.isoformat()
        }), 201
        
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@trip_bp.route('/api/trips', methods=['GET'])
@login_required
def get_trips():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'trips': [{
            'id': trip.id,
            'destination': trip.destination,
            'start_date': trip.start_date.isoformat(),
            'end_date': trip.end_date.isoformat(),
            'location_count': len(trip.locations)
        } for trip in trips]
    }), 200

@trip_bp.route('/api/trips/<int:trip_id>', methods=['GET'])
@login_required
def get_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found or access denied'}), 404
    
    return jsonify({
        'id': trip.id,
        'destination': trip.destination,
        'start_date': trip.start_date.isoformat(),
        'end_date': trip.end_date.isoformat(),
        'locations': [{
            'id': location.id,
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude
        } for location in trip.locations]
    }), 200

@trip_bp.route('/api/trips/<int:trip_id>', methods=['PUT'])
@login_required
def update_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found or access denied'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update fields if provided
        if 'destination' in data:
            trip.destination = data['destination']
        
        if 'start_date' in data:
            trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            
        if 'end_date' in data:
            trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        # Validate dates
        if trip.end_date < trip.start_date:
            return jsonify({'error': 'End date cannot be before start date'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trip updated successfully',
            'trip': {
                'id': trip.id,
                'destination': trip.destination,
                'start_date': trip.start_date.isoformat(),
                'end_date': trip.end_date.isoformat()
            }
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@trip_bp.route('/api/trips/<int:trip_id>', methods=['DELETE'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found or access denied'}), 404
    
    try:
        # Delete associated locations first
        for location in trip.locations:
            db.session.delete(location)
        
        # Delete the trip
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({'message': 'Trip and all associated locations deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# ----- TRIP STATISTICS -----

@trip_bp.route('/api/trips/stats', methods=['GET'])
@login_required
def get_trip_stats():
    """Get statistics about the user's trips"""
    
    # Count of trips
    trip_count = Trip.query.filter_by(user_id=current_user.id).count()
    
    # Count of unique destinations
    unique_destinations = db.session.query(Trip.destination).filter_by(
        user_id=current_user.id
    ).distinct().count()
    
    # Total days traveled (sum of trip durations)
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    total_days = sum([(trip.end_date - trip.start_date).days + 1 for trip in trips])
    
    # Count of total locations
    location_count = Location.query.join(Trip).filter(
        Trip.user_id == current_user.id
    ).count()
    
    return jsonify({
        'total_trips': trip_count,
        'unique_destinations': unique_destinations,
        'total_days_traveled': total_days,
        'total_locations': location_count
    }), 200

# ----- UPCOMING TRIPS -----

@trip_bp.route('/api/trips/upcoming', methods=['GET'])
@login_required
def get_upcoming_trips():
    """Get trips that are upcoming (start date is in the future)"""
    
    today = datetime.now().date()
    upcoming_trips = Trip.query.filter(
        Trip.user_id == current_user.id,
        Trip.start_date >= today
    ).order_by(Trip.start_date).all()
    
    return jsonify({
        'upcoming_trips': [{
            'id': trip.id,
            'destination': trip.destination,
            'start_date': trip.start_date.isoformat(),
            'end_date': trip.end_date.isoformat(),
            'days_until': (trip.start_date - today).days
        } for trip in upcoming_trips]
    }), 200