from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# New User
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable = False, default='')
    password = db.Column(db.String, nullable = True, default='')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email='', first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Crag(db.Model):
    id = db.Column(db.String, primary_key = True)
    crag_name = db.Column(db.String(150), nullable = False)
    latitude = db.Column(db.String(150))
    longitude = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    rock_type = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, crag_name, latitude, longitude, city, state, rock_type, user_token, id = ''):
        self.id = self.set_id()
        self.crag_name = crag_name
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.state = state
        self.rock_type = rock_type
        self.user_token = user_token

    def __repr__(self):
        return f'The Following crag has been added to the database: {self.crag_name}'
        
    def set_id(self):
        return (secrets.token_urlsafe())
        
class CragSchema(ma.Schema):
    class Meta:
        fields = ['id', 'crag_name', 'latitude', 'longitude', 'city', 'state', 'rock_type']

crag_schema = CragSchema()
crags_schema = CragSchema(many=True)