from flask import Blueprint

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return "Hello, World! Welcome to SoulTrip API."