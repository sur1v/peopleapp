#~peopleapp/app.py
# author: Jose Ignacio Martinez <gsuriv@gmail.com>

from flask import Flask, request, Response
from database.db import initialize_db
from database.models import People

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
    # Raise exception if not found
    except Exception:
        return 'Not found', 404

# Add person
@app.route('/people', methods=['POST'])
def add_people():
    body = request.get_json(force=True)
    people = People(**body).save()
    nationalId = people.nationalId
    return {'nationalId': str(nationalId)}, 200

# Update person
@app.route('/people/<id>', methods=['PUT'])
def update_people(id):
    body = request.get_json(force=True)
    People.objects.get(nationalId=id).update(**body)
    return '', 200

# Delete person
@app.route('/people/<id>', methods=['DELETE'])
def delete_people(id):
    People.objects.get(nationalId=id).delete()
    return '', 200

app.run()