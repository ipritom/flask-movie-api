# Flask Movie Api
---
This is a template API using Flask and [OMDb API](https://www.omdbapi.com/). API testing is performend by [Postman](https://www.postman.com/).

## How to Use 
At first need to set flask environment as following.
In Windows
```
set FLASK_ENV=development
```
In Linux
```
export FLASK_ENV=development 
```
In api folder run bellow line in terminal.
```
python app.py
```

## API Testing in Postman

### Login
```
POST http://127.0.0.1:4455/login
```
Body/Form-data
```
username : admin
password : 112233
```
### Logout
```
GET http://127.0.0.1:4455/login
```

### Search Movie
```
POST http://127.0.0.1:4455/search
```
Body/Form-data
```
movie_name : <name_for_search>
```

### Add Movie
```
POST http://127.0.0.1:4455/add
```
Body/Form-data
```
movie_name : <name_for_add>
```

### Delete Movie
```
POST http://127.0.0.1:4455/delete
```

Body/Form-data
```
record_id : <valid_record_id>
```

### See List of Movies for a Specific User (Login Required)
```
GET http://127.0.0.1:4455/user
```
