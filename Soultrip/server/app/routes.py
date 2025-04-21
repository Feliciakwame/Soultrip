from flask import Blueprint, jsonify,request
from .models import db,User,Trip
from .extensions import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

api = Blueprint("api", __name__)

@api.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "SoulTrip API", 
        "endpoints": {
            "signup": "/api/signup",
            "login": "/api/login",
            "users": "/api/users"
        }
    })

@api.route('/signup',methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    user=User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({"message":'Invalid credentials'}),401
    
    access_token=create_access_token(identity=user.id)
    return jsonify({
        "message":"Login successful",
        "access_token":access_token,
        "user_id":user.id,
        "username":user.username
        }),200


@api.route("/users",methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password,
        }
        user_list.append(user_data)
    return jsonify(user_list)

@api.route("/users",methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(username=data["username"], email=data["email"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201
