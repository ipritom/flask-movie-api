from flask_sqlalchemy import SQLAlchemy

#SQLAlchemy integration to the Flask applications
db = SQLAlchemy()

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    
class history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    key = db.Column(db.String(50)) #search key

class movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(50)) #search key
    user_id = db.Column(db.String(50))
    movie = db.Column(db.JSON)
