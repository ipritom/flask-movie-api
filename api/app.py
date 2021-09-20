'''
Flask Based Movie API 
Project Created: 14-09-2021
'''
# from environmet
from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
import requests
from werkzeug.security import generate_password_hash, check_password_hash

# from dev
from models import db, User, MovieRecord, UserMovie


# configure flask app 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movieapi.sqlite" #database location uri
# initialize the app for the use with this database setup
migrate = Migrate(app, db)
db.init_app(app)

#omdb API Key (https://www.omdbapi.com/)
omdb_api_key='2a50a570'

# default landing url
@app.route('/')
def index():
    return "Welcome to Movie API"

# user url
@app.route('/user', methods=['GET'])
def get_one_user():
    if "username" in session:
        # initiate a message dictionary
        message = {}
        # fetching movie data by user_id
        user_movies = db.session.query(UserMovie).filter(UserMovie.user_id==session['user_id']).all()

        # iterate over all movies
        for record in user_movies:
            movie = db.session.query(MovieRecord).filter(MovieRecord.id==record.movie_id).first()
            message[str(record.id)] = movie.title #movie title with record id
        
        # return message with a greeting
        message["message"] = f"Hello {session['username']}!"

        return jsonify(message)
    else:
        return jsonify({"message":"Invalid"})

# users list url
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

# user login url
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login from a Form"""
    # if a session is running already
    if "username" in session:
        return jsonify({"message":'You are already in! Hurrah!'})

    if request.method=='POST':
        # get username and password from request object
        username = request.form['username']
        password = request.form['password']
        # check user existence in DB and match password hash
        userExist = db.session.query(db.exists().where(User.name == username)).scalar()
        passMatch = check_password_hash(generate_password_hash(password,method="sha256"),password)
        
        # if password and username match : create a session
        if userExist and passMatch:
            user_info = db.session.query(User).filter(User.name==username).first() 
            session['admin'] = user_info.admin
            session['user_id'] = user_info.id
            session['username'] = username
         
            return jsonify({"message":f'Welcome {username}!'})
        else:
            return jsonify({"message":'invalid'})

# user logout url
@app.route('/logout', methods=['GET'])
def logout():
    """Logout Function"""
    if "username" in session:
        session.clear()
        return jsonify({"message":'Logged Out'})
    else:
        return jsonify({"message":'All Ready Logged Out'})


# new user register/signup url
@app.route('/register', methods=['POST','GET'])
def register():
    # if a session is running already
    if "user_id" in session:
        return redirect(url_for('get_one_user'))

    if request.method == 'POST':
        # getting data from request form
        username = request.form['username']
        password = request.form['password']
        # checking existence
     
        exists = db.session.query(db.exists().where(User.name == username)).scalar()
        # if user already exists return with message
        if exists:
            return jsonify({'message':"User Already Exists!"})

        # creating password hash
        hashed_password = generate_password_hash(password, method='sha256')
        # create new user object
        new_user = User(public_id=str(uuid.uuid4()), name=username, password=hashed_password, admin=False)
        # add new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message' : 'New User Created!'})

# search movie with name by requesting OMDB API
@app.route('/search', methods=['GET','POST'])
def search():
    """Function to search movie by a key movie_name"""
    
    if request.method=='POST':
        # take movie name 
        movie_name = request.form['movie_name']
        # api url with api key
        api_url = f'https://www.omdbapi.com/?t={movie_name}&apikey={omdb_api_key}'
        # get response from omdb as json
        omdb_response = requests.get(api_url).json()
        #if valid response
        if "Error" in omdb_response: 
            return jsonify({"message":"Movie not found!"})

        return omdb_response
    
    return jsonify({"message":'invalid'})

# add movie by user
@app.route('/add', methods=['GET','POST'])
def add():
    """Function to add a movie by search key given by user"""

    # if no session is running
    if "user_id" not in session:
        return redirect(url_for('index'))

    if request.method=='POST':
        # take movie name 
        movie_name = request.form['movie_name']
        # search with key in the database 
        record = db.session.query(MovieRecord).filter(MovieRecord.key==movie_name).first()

        # taking user_id from session data
        user_id = session['user_id']
        # if movie already exists update the UserMovie
        if record!=None:
            new_add = UserMovie(movie_id=record.id,user_id=user_id)
            db.session.add(new_add)
            # commit to database
            db.session.commit()
            return record.movie
        else:
            # api url with api key
            api_url = f'https://www.omdbapi.com/?t={movie_name}&apikey={omdb_api_key}'
            # get response from omdb as json
            omdb_response = requests.get(api_url).json()
            # if valid response
            if "Error" in omdb_response: 
                return jsonify({"message":"Movie not found!"})

            # saving valid movie records with key
            new_record = MovieRecord(key=movie_name,title=omdb_response['Title'],movie=omdb_response)
            db.session.add(new_record)
            db.session.flush()
            # saving movie id to user movie table
            new_add = UserMovie(movie_id=new_record.id,user_id=user_id)
            db.session.add(new_add)
            # commit to database
            db.session.commit()

            return omdb_response
    
    return jsonify({"message":'invalid'})

# delete movie by user
@app.route('/delete', methods=['POST'])
def delete():
    """Function to delete a movie by record id given by user"""

    # if no session is running
    if "user_id" not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        record_id = request.form['record_id']
        # existence of the record_id under the session user_id
        exists = db.session.query(db.exists().where((UserMovie.user_id == session['user_id']) & 
                                                    (UserMovie.id == record_id))).scalar()
        
        if exists:
            db.session.query(UserMovie).filter(UserMovie.id==record_id).delete()
            # commit to database
            db.session.commit()
            return jsonify({"message": "Movie Deleted"})
        else:
            return jsonify({'message':'There is no such movie in your list.'})

        
        


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=4455,debug=True)  # host and port are manually assigned 
    