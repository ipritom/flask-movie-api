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
    
class MovieRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100)) #search key
    title = db.Column(db.String(256))
    movie = db.Column(db.JSON)

class UserMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.String(50))
    
