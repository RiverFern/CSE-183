"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma
from py4web import Field

url_signer = URLSigner(session)


@action('index')
@action.uses(db, auth, session, 'index.html')
def index():
    print("User:", get_user_email())

    rows = db(db.contact.user_email == get_user_email()).select().as_list()

    for row in rows:
        s = ""
        row["phone_numbers"] = s
        print(row)

    return dict(rows=rows,
                url_signer=url_signer)


@action('add_contact', method=["GET", "POST"])
@action.uses(db, auth, session, 'add_contact.html')
def add_contact():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)


@action('edit_phones/<contact_id:int>')
@action.uses(db, auth, session, 'edit_phones.html')
def edit_phones(contact_id=None):
    assert contact_id is not None

    numbers = db(db.phone.contact_id == contact_id).select().as_list()

    return dict(contact_id=contact_id, numbers=numbers, url_signer=url_signer)


@action('add_phone/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, auth, session, 'add_phone.html')
def add_phone(contact_id=None):
    assert contact_id is not None

    form = Form([Field('phone'), Field('kind')], csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:

        db.phone.insert(
            phone_number=form.vars['phone'],
            phone_name=form.vars['kind'],
            contact_id=contact_id,
        )
        redirect(URL('edit_phones', contact_id))

    return dict(form=form)


@action('edit_contact/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit_contact.html')
def edit_contact(contact_id=None):
    assert contact_id is not None
    p = db.contact[contact_id]
    if p is None:
        redirect(URL('index'))
    form = Form(db.contact, csrf_session=session, record=p, deletable=False, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)


@action('delete/<contact_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(contact_id=None):
    assert contact_id is not None
    db(db.contact.id == contact_id).delete()
    redirect(URL('index'))


@action('edit_phone/<contact_id:int>/<phone_id:int>', method=["GET","POST"])
@action.uses(db, session, auth.user, 'edit_phone.html')
def edit_phone(phone_id=None, contact_id=None):
    assert phone_id is not None
    assert contact_id is not None

    p = db.phone[phone_id]
    if p is None:
        redirect(URL('index'))

    form = Form(db.phone, csrf_session=session, record=p, deletable=False, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('edit_phones', contact_id))
    return dict(form=form)


@action('delete_phone/<contact_id:int>/<phone_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(phone_id=None, contact_id=None):
    assert phone_id is not None
    assert contact_id is not None
    db(db.phone.id == phone_id).delete()
    redirect(URL('edit_phones', contact_id))
