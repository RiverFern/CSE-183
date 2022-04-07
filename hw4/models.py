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


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'contact',
    Field('first_name'),
    Field('last_name'),
    Field('user_email', default=get_user_email),
)

db.contact.id.readable = db.contact.id.writable = False
db.contact.user_email.readable = db.contact.user_email.writable = False


db.define_table(
    'phone',
    Field('phone_number'),
    Field('phone_name'),
    Field('contact_id', 'reference contact'),
)

db.phone.contact_id.readable = db.phone.contact_id.writable = False
db.phone.id.readable = db.phone.id.writable = False

db.commit()
