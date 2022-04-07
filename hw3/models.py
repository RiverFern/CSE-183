"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None


def get_time():
    return datetime.datetime.utcnow()

# Define your table below
#
# db.define_table('thing', Field('name'))
#
# always commit your models to avoid problems later


db.define_table(
    'bird',
    Field('bird_name', requires=IS_NOT_EMPTY()),
    Field('weight', 'float', default=0.0, requires=IS_FLOAT_IN_RANGE(0, 1e6)),
    Field('diet', requires=IS_NOT_EMPTY()),
    Field('habitat', requires=IS_NOT_EMPTY()),
    Field('n_sightings', 'integer', default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    Field('seen_by', default=get_user_email),
)

db.bird.id.readable = db.bird.id.writable = False
db.bird.seen_by.readable = db.bird.seen_by.writable = False

db.bird.bird_name.label = 'Bird Name'
db.bird.weight.label = 'Weight'
db.bird.diet.label = 'Diet'
db.bird.habitat.label = 'Habitat'
db.bird.n_sightings.label = "Number of Sightings"

db.commit()
