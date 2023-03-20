from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

db= SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20), nullable=False, unique=True,primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    image_url = db.Column(db.Text,default="/static/images/default-pic.png",)
    
    @classmethod
    def register(cls,username,password,email,image_url):
        """register user w/hashed password & return user"""
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal unicode utf8 string
        hashed_utf8  = hashed.decode('utf8')
        user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            image_url = image_url
        )
        db.session.add(user)
        return user
    @classmethod
    def authenticate(cls,username,pwd):
        """Validate that user exists & password is correct"""

        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False


class Puuid(db.Model):
    __tablename__ = 'puuids'
    puuid = db.Column(db.String, nullable = False,unique=True,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)