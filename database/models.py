#~peopleapp/database/models.py
# author: Jose Ignacio Martinez <gsuriv@gmail.com>

from .db import db

class People(db.Document):
    nationalId = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    lastName = db.StringField(required=True)
    age = db.StringField(required=True)
    originPlanet = db.StringField(required=True)
    pictureUrl = db.StringField(required=True)
