'''
Flask Based Movie API 
Project Created: 14-09-2021
'''
# from environmet
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# from dev
from models import db, User
# from routes import *


# configure flask app 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movieapi.sqlite" #database location uri
# initialize the app for the use with this database setup
db.init_app(app)


@app.route('/')
def index():
    return "Welcome to Movie API"

#users page
@app.route('/user/<user_id>', methods=['POST'])
def get_one_users():
    if request.method == "POST":
        print("HELLO")
        data = request.get_json()
        print(data)
        name = data['name']
        print(name)
        exists = db.session.query(db.exists().where(User.name == name)).scalar()

        return jsonify({'existance':exists})
    
    return jsonify({"message":"None"})

@app.route('/users',  methods=['GET'])
def get_all_user():
    """Return Users List from Database"""
    if request.method == "GET":
        users = User.query.all() # querry on user table for all users
        users_dict = dict() # empty dictionary 
        # preparing users dictionary
        for user in users:
            users_dict[user.id] = {'Name': user.name,
                                   'admin':user.admin}

        return jsonify(users_dict)

    return jsonify({"message":"Invalid"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login from a Form"""
    if request.method=='POST':
        # get username and password from request object
        username = request.form['username']
        password = request.form['password']
        # check user existence in DB and match password hash
        userExist = db.session.query(db.exists().where(User.name == username)).scalar()
        passMatch = check_password_hash(generate_password_hash(password,method="sha256"),password)
        
        if userExist and passMatch:
            session['username'] = username
            return jsonify({"message":'valid'})
        else:
            return jsonify({"message":'invalid'})

@app.route('/logout', methods=['GET'])
def logout():
    if "username" in session:
        session.pop("username", None)
        return jsonify({"message":'Logged Out'})
    else:
        return jsonify({"message":'All Ready Logged Out'})



@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        #getting data from request object
        data = request.get_json()
        #checking existence
        name = data['name']
        exists = db.session.query(db.exists().where(User.name == name)).scalar()
        #if user already exists return with message
        if exists:
            return jsonify({'message':"User Already Exists!"})

        #creating password hash
        hashed_password = generate_password_hash(data['password'], method='sha256')
        #create new user object
        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
        #add new user to the database
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message' : 'New User Created!'})
    
  
@app.route('/user/<user_id>', methods=['PUT'])
def promote_user():
    return ''

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user():
    return ''

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=4455,debug=True)  # host and port are manually assigned 
    