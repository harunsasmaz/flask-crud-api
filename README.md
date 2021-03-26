# Flask CRUD API

A very simple RESTful API for CRUD operations.

### Requirements

> Anaconda 3 (Optional)

> Python (3.7 Preferred)

> SQLite (Downloaded withing Python, no need to install)

> (Flask) pip3 install flask

> (Flask SQLAlchemy) pip3 install flask_sqlalchemy

> Text Editor (VSCode preferred)

> Curl or Postman (HTTP Request/Response)

### Testing

> conda create --name <environment name> python=3.7

> conda activate <environment name>

> python3 app.py

> Send request via Curl or Postman to http://localhost:8080/users

### Endpoints

This api utilizes only a single endpoint '/users'.

For GET, PUT, DELETE requests, you should add {id} parameter, i.e. /users/2