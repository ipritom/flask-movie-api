from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///example.sqlite"

# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Interger,primary_key = True)
#     public_id = db.Column(db.String(50), unique=True)
#     name = db.Column(db.String(50))
#     password = db.Column(db.String(80))
#     admin = db.Comun(db.Boolean)

# class Todo(db.Model):
#     id = db.Column(db.Integer, )

app = Flask(__name__)