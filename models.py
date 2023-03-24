from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    image_url = db.Column(db.Text,default="/static/images/default-pic.png",)
    bio = db.Column(db.Text,nullable=True)
    summoner = db.Column(db.String, nullable=True)
    
    @classmethod
    def register(cls,username,password,email,image_url):
        """register user w/hashed password & return user"""
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            username=username,
            password=hashed,
            email=email,
            image_url = image_url
        )
        db.session.add(user)
        return user
    @classmethod
    def authenticate(cls,username,password):
        """Validate that user exists & password is correct"""

        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False


class Puuid(db.Model):
    __tablename__ = 'puuids'
    puuid = db.Column(db.String, nullable = False,unique=True,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)