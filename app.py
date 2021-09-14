'''
Flask Based Movie API 
Project Created: 14-09-2021
'''

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


#configure flask apop 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movieapi.sqlite" #database location uri

 #SQLAlchemy integration to the Flask applications
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete  = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    
#default landing page
@app.route('/')
def index():
    return "Welcome to Movie API"

#users page
@app.route('/user', methods=['GET'])
def get_all_users():
    return ''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        return username

@app.route('/user/<user_id>')
def get_one_user():
    return ''

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        #creating password hash
        hashed_password = generate_password_hash(data['password'], method='sha256')
        #create new user object
        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
        #add new user to the database
        db.session.add(new_user)
        db.session.commit()
        # db.session.close()
        return jsonify({'message' : 'New User Created!'})
  
@app.route('/user/<user_id>', methods=['PUT'])
def promote_user():
    return ''

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user():
    return ''
    
    
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=4455,debug=True)  # host and port are manually assigned 
    