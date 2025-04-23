from .extensions import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    trips=db.relationship('Trip',backref='user',lazy=True)
    journal_entries=db.relationship('JournalEntry', backref='user', lazy=True)
    trusted_contacts=db.relationship('TrustedContact', back_populates='user', cascade='all, delete-orphan', lazy=True)
    password_hash=db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is a write-only')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    locations = db.relationship('Location', backref='trip', lazy=True)

class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "created_at":self.created_at.strftime('%Y -%m-%d')if self.created_at else None,
        }
    
class TrustedContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user=db.relationship('User', backref='trusted_contacts', lazy=True)
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    
def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
def check_password(self, password):
    return check_password_hash(self.password_hash, password)

def to_dict(self):
    return {
        'id': self.id,
        'username': self.username,
        'email': self.email
    }

    
