#~peopleapp/app.py
# author: Jose Ignacio Martinez <gsuriv@gmail.com>

from flask import Flask, request, Response
from database.db import initialize_db
from database.models import People
from mongoengine import NotUniqueError
from mongoengine import DoesNotExist

app = Flask(__name__)

# Database settings
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://127.0.0.1/peopleapp'
}

initialize_db(app)

# List people
@app.route('/people')
def get_people():
    people = People.objects().to_json()
    return Response(people, mimetype="application/json", status=200)

# Get single person
@app.route('/people/<id>', methods=['GET'])
def get_single_people(id):
    try:
        body = People.objects.get(nationalId=id).to_json()
        return Response(body, mimetype="application/json", status=200)
    # Returns 404 if not found
    except DoesNotExist:
        return 'Not found', 404

# Add person
@app.route('/people', methods=['POST'])
def add_people():
    try:
        # Check request header
        if request.headers.get('Content-Type')=='application/json':
            body = request.get_json(force=True)
            try:
                people = People(**body).save()
                nationalId = people.nationalId
                body = People.objects.get(nationalId=nationalId).to_json()
                # Returns created object and 201
                return Response(body, mimetype="application/json", status=201)
            # Handle validation
            except NotUniqueError:
                return 'Validation error', 400
        # Returns 400 on header mismatch
        else:
            return 'Header error', 400
    # Returns 500 in any other exception
    except Exception:
        return 'Error', 500


# Update person
@app.route('/people/<id>', methods=['PUT'])
def update_people(id):
    try:
        # Check request header
        if request.headers.get('Content-Type')=='application/json':
            body = request.get_json(force=True)
            try:
                People.objects.get(nationalId=id).update(**body)
                return 'Success', 200
            except DoesNotExist:
                return 'Validation error', 400
       # Returns 400 on header mismatch
        else:
            return 'Header error', 400
    # Returns 500 in any other exception
    except Exception:
        return 'Error', 500

# Delete person
@app.route('/people/<id>', methods=['DELETE'])
def delete_people(id):
    try:
        People.objects.get(nationalId=id).delete()
        return 'Success', 200
    # Returns 404 if not found
    except DoesNotExist:
        return 'Not found', 404

app.run()