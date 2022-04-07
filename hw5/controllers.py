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
from .models import get_user_email, get_user

url_signer = URLSigner(session)


@action('index')
@action.uses(db, auth, 'index.html')
def index():

    return dict(
        # COMPLETE: return here any signed URLs you need.
        add_post_url=URL('add_post', signer=url_signer),
        load_posts_url=URL('load_posts', signer=url_signer),
        get_rating_url=URL('get_rating', signer=url_signer),
        set_rating_url=URL('set_rating', signer=url_signer),
        del_post_url=URL('del_post', signer=url_signer),
        show_likers_url=URL('show_likers', signer=url_signer),
        show_haters_url=URL('show_haters', signer=url_signer),
    )


@action('load_posts')
@action.uses(db, url_signer.verify())
def load_posts():
    posts = db(db.posts).select().as_list()
    email = get_user_email()
    return dict(posts=posts, email=email)


@action('add_post', method="POST")
@action.uses(url_signer.verify(), db)
def add_post():

    user = db(db.auth_user.email == get_user_email()).select()
    for r in user:
        name = r['first_name'] + " " + r['last_name']

    id = db.posts.insert(
        post_content=request.json.get('post_content'),
        name=name,
        email=get_user_email()
    )

    email = get_user_email()

    return dict(id=id, name=name, email=email)


@action('get_rating')
@action.uses(url_signer.verify(), db, auth.user)
def get_rating():
    post_id = request.params.get('post_id')

    row = db((db.rating.post == post_id) &
             (db.rating.rater == get_user())).select().first()
    rating = row.rating if row is not None else 0

    return dict(rating=rating)


@action('set_rating', method="POST")
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    post_id = request.json.get('post_id')

    rating = request.json.get('rating')
    db.rating.update_or_insert(
        ((db.rating.post == post_id) & (db.rating.rater == get_user())),
        post=post_id,
        rater=get_user(),
        rating=rating,
    )


@action('show_likers', method=["POST", "GET"])
@action.uses(url_signer.verify(), db, auth.user)
def show_likers():
    post_id = request.json.get('post_id')
    ratings = db((db.rating.post == post_id) & (db.rating.rating == 1)).select()

    likers = []

    for r in ratings:
        name = ""
        user = db(db.auth_user.id == r.rater).select().as_list()
        for u in user:
            name += u['first_name'] + " " + u['last_name']
            likers.append(name)

    likers_string = ' '.join(str(e) for e in likers)

    return dict(likers=likers_string)


@action('show_haters', method=["POST", "GET"])
@action.uses(url_signer.verify(), db, auth.user)
def show_haters():
    post_id = request.json.get('post_id')
    ratings = db((db.rating.post == post_id) & (db.rating.rating == 2)).select()

    haters = []

    for r in ratings:
        name = ""
        user = db(db.auth_user.id == r.rater).select().as_list()
        for u in user:
            name += u['first_name'] + " " + u['last_name']
            haters.append(name)

    haters_string = ' '.join(str(e) for e in haters)

    return dict(haters=haters_string)


@action('del_post')
@action.uses(url_signer.verify(), db)
def delete_post():
    id = request.params.get('id')
    assert id is not None
    db(db.posts.id == id).delete()
    return "ok"
