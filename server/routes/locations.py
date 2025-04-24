from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.models import db, Location, Trip
from sqlalchemy.exc import SQLAlchemyError
import math

locations_bp = Blueprint('locations', __name__)

# ----- LOCATION ROUTES -----

@locations_bp.route('/api/locations', methods=['GET'])
@login_required
def get_all_locations():
    """Get all locations across all trips for the current user"""
    
    # Using a join to ensure we only get locations from the user's trips
    locations = Location.query.join(Trip).filter(Trip.user_id == current_user.id).all()
    
    return jsonify({
        'locations': [{
            'id': location.id,
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'trip_id': location.trip_id
        } for location in locations]
    }), 200

@locations_bp.route('/api/locations/create', methods=['POST'])
@login_required
def create_location():
    """Create a new location (without associating to a trip)"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ('name', 'latitude', 'longitude', 'trip_id')):
        return jsonify({'error': 'Missing required location fields'}), 400
    
    # Verify trip ownership
    trip = Trip.query.filter_by(id=data['trip_id'], user_id=current_user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found or access denied'}), 404
    
    try:
        # Validate coordinates
        lat = float(data['latitude'])
        lng = float(data['longitude'])
        
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({'error': 'Invalid coordinates'}), 400
        
        # Create location
        location = Location(
            name=data['name'],
            latitude=lat,
            longitude=lng,
            trip_id=data['trip_id']
        )
        
        db.session.add(location)
        db.session.commit()
        
        return jsonify({
            'message': 'Location created successfully',
            'location': {
                'id': location.id,
                'name': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'trip_id': location.trip_id
            }
        }), 201
        
    except ValueError:
        return jsonify({'error': 'Invalid coordinate format'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@locations_bp.route('/api/trips/<int:trip_id>/locations', methods=['POST'])
@login_required
def add_location_to_trip(trip_id):
    """Add a location to a specific trip"""
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found or access denied'}), 404
    
    data = request.get_json()
    
    if not data or not all(k in data for k in ('name', 'latitude', 'longitude')):
        return jsonify({'error': 'Missing required location fields'}), 400
    
    try:
        # Validate coordinates
        lat = float(data['latitude'])
        lng = float(data['longitude'])
        
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({'error': 'Invalid coordinates'}), 400
        
        # Create location
        location = Location(
            name=data['name'],
            latitude=lat,
            longitude=lng,
            trip_id=trip_id
        )
        
        db.session.add(location)
        db.session.commit()
        
        return jsonify({
            'message': 'Location added successfully',
            'location': {
                'id': location.id,
                'name': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude
            }
        }), 201
        
    except ValueError:
        return jsonify({'error': 'Invalid coordinate format'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@locations_bp.route('/api/trips/<int:trip_id>/locations', methods=['GET'])
@login_required
def get_trip_locations(trip_id):
    """Get all locations for a specific trip"""
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found or access denied'}), 404
    
    return jsonify({
        'locations': [{
            'id': location.id,
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude
        } for location in trip.locations]
    }), 200

@locations_bp.route('/api/locations/<int:location_id>', methods=['GET'])
@login_required
def get_location(location_id):
    """Get details for a specific location"""
    
    # Find location and verify ownership through trip
    location = Location.query.join(Trip).filter(
        Location.id == location_id,
        Trip.user_id == current_user.id
    ).first()
    
    if not location:
        return jsonify({'error': 'Location not found or access denied'}), 404
    
    # Get the trip details for this location
    trip = Trip.query.get(location.trip_id)
    
    return jsonify({
        'id': location.id,
        'name': location.name,
        'latitude': location.latitude,
        'longitude': location.longitude,
        'trip': {
            'id': trip.id,
            'destination': trip.destination
        }
    }), 200

@locations_bp.route('/api/locations/<int:location_id>', methods=['PUT'])
@login_required
def update_location(location_id):
    """Update a location's details"""
    
    # Find location and verify ownership through trip
    location = Location.query.join(Trip).filter(
        Location.id == location_id,
        Trip.user_id == current_user.id
    ).first()
    
    if not location:
        return jsonify({'error': 'Location not found or access denied'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update fields if provided
        if 'name' in data:
            location.name = data['name']
            
        if 'latitude' in data:
            lat = float(data['latitude'])
            if not (-90 <= lat <= 90):
                return jsonify({'error': 'Invalid latitude'}), 400
            location.latitude = lat
            
        if 'longitude' in data:
            lng = float(data['longitude'])
            if not (-180 <= lng <= 180):
                return jsonify({'error': 'Invalid longitude'}), 400
            location.longitude = lng
        
        db.session.commit()
        
        return jsonify({
            'message': 'Location updated successfully',
            'location': {
                'id': location.id,
                'name': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude
            }
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid coordinate format'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@locations_bp.route('/api/locations/<int:location_id>', methods=['DELETE'])
@login_required
def delete_location(location_id):
    """Delete a location"""
    
    # Find location and verify ownership through trip
    location = Location.query.join(Trip).filter(
        Location.id == location_id,
        Trip.user_id == current_user.id
    ).first()
    
    if not location:
        return jsonify({'error': 'Location not found or access denied'}), 404
    
    try:
        db.session.delete(location)
        db.session.commit()
        
        return jsonify({'message': 'Location deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@locations_bp.route('/api/locations/nearby', methods=['GET'])
@login_required
def get_nearby_locations():
    """Find locations near a specified point"""
    
    try:
        # Get query parameters
        lat = float(request.args.get('latitude'))
        lng = float(request.args.get('longitude'))
        radius = float(request.args.get('radius', 10.0))  # Default 10km radius
        
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180) or radius <= 0:
            return jsonify({'error': 'Invalid coordinates or radius'}), 400
        
        # Get all user locations
        locations = Location.query.join(Trip).filter(Trip.user_id == current_user.id).all()
        
        # Calculate distance for each location and filter by radius
        nearby = []
        for location in locations:
            distance = haversine_distance(lat, lng, location.latitude, location.longitude)
            if distance <= radius:
                nearby.append({
                    'id': location.id,
                    'name': location.name,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'distance': round(distance, 2),
                    'trip_id': location.trip_id
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance'])
        
        return jsonify({
            'center': {'latitude': lat, 'longitude': lng},
            'radius': radius,
            'locations': nearby,
            'count': len(nearby)
        }), 200
        
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid parameters'}), 400

@locations_bp.route('/api/trips/<int:trip_id>/locations/bulk', methods=['POST'])
@login_required
def bulk_add_locations(trip_id):
    """Add multiple locations to a trip at once"""
    
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found or access denied'}), 404
    
    data = request.get_json()
    
    if not data or not isinstance(data, list):
        return jsonify({'error': 'Invalid data format. Expected list of locations'}), 400
    
    try:
        added_locations = []
        
        for loc_data in data:
            if not all(k in loc_data for k in ('name', 'latitude', 'longitude')):
                continue
                
            try:
                # Validate coordinates
                lat = float(loc_data['latitude'])
                lng = float(loc_data['longitude'])
                
                if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                    continue
                
                # Create location
                location = Location(
                    name=loc_data['name'],
                    latitude=lat,
                    longitude=lng,
                    trip_id=trip_id
                )
                
                db.session.add(location)
                added_locations.append(location)
                
            except ValueError:
                continue
        
        if not added_locations:
            return jsonify({'error': 'No valid locations provided'}), 400
            
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully added {len(added_locations)} locations',
            'locations': [{
                'id': loc.id,
                'name': loc.name,
                'latitude': loc.latitude,
                'longitude': loc.longitude
            } for loc in added_locations]
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# ----- UTILITY FUNCTIONS -----

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r