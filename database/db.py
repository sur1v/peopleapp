#~peopleapp/database/db.py
# author: Jose Ignacio Martinez <gsuriv@gmail.com>

from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_db(app):
    db.init_app(app)
