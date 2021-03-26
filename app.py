from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def get_date():
    now = datetime.now()
    return now.strftime("%B %d, %Y %H:%M:%S")

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    givenName = db.Column(db.String(80), nullable=False)
    familyName = db.Column(db.String(80), nullable=False)
    created = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'id': self.id, 'email': self.email,
                'givenName': self.givenName, 'familyName': self.familyName,
                'created': self.created}
        # this method we are defining will convert our output to json

    def add_user(_email, _fname, _lname, _created):
        '''function to add user to database using parameters'''
        # creating an instance of our User constructor
        new_user = User(email=_email, givenName=_fname, familyName =_lname, created=_created)
        db.session.add(new_user)  # add new user to database session
        db.session.commit()  # commit changes to session

    def get_all_users():
        '''function to get all users in our database'''
        return [User.json(user) for user in User.query.all()]

    def get_user(_id):
        '''function to get user using the id of the user as parameter'''
        try:
            return [User.json(User.query.filter_by(id=_id).first())]
        except:
            return {"Warning": "No such user"}

    def update_user(_id, _email, _fname, _lname):
        '''function to update the details of a user using parameters'''
        try:
            user_to_update = User.query.filter_by(id=_id).first()
            user_to_update.email = _email
            user_to_update.givenName = _fname
            user_to_update.familyName = _lname
            db.session.commit()
            return 'Success'
        except:
            return 'Failed'

    def delete_user(_id):
        '''function to delete a user from our database using
           the id of the user as a parameter'''
        try:
            User.query.filter_by(id=_id).delete()
            db.session.commit()
            return 'Success'
        except:
            return 'Failed'

#create all db tables
@app.before_first_request
def create_tables():
    db.create_all()

# route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    '''Function to get all the users in the database'''
    return jsonify({'users': User.get_all_users()})

# route to get user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return_value = User.get_user(id)
    return jsonify(return_value)

# route to add new user
@app.route('/users', methods=['POST'])
def add_user():
    '''Function to add new user to our database'''
    request_data = request.get_json()
    if request_data['email'] is None:
        return Response("Email is not provided", 400, mimetype='application/json')

    if request_data['givenName'] is None:
        return Response("First name is not provided", 400, mimetype='application/json')

    if request_data['familyName'] is None:
            return Response("Last name is not provided", 400, mimetype='application/json')

    User.add_user(request_data["email"], request_data['givenName'],
                    request_data['familyName'], get_date())

    response = Response("user added", 201, mimetype='application/json')
    return response

# route to update user with PUT method
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    '''Function to edit user in our database using user id'''
    request_data = request.get_json()
    ret = User.update_user(id, request_data["email"], request_data['givenName'], request_data['familyName'])
    if(ret == 'Success'):
        response = Response("User updated", status=200, mimetype='application/json')
    else:
        response = Response("Update request failed", status=400, mimetype='application/json')
    return response


# route to delete user using the DELETE method
@app.route('/users/<int:id>', methods=['DELETE'])
def remove_user(id):
    '''Function to delete user from our database'''
    ret = User.delete_user(id)
    if(ret == 'Success'):
        response = Response("User deleted", status=200, mimetype='application/json')
    else:
        response = Response("User not found", status=404, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run(port=8080, debug=False)