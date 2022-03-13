from functools import wraps
from flask import redirect, render_template, request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from modules import db, bcrypt
from modules.models import User, Follower, Tweet

from .forms import RegisterForm, LoginForm

users_routes = Blueprint('users', __name__)

@users_routes.route('/', methods = ['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(userName = request.form['name']).first()

            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                session['loggedIn'] = True
                session['user_id'] = user.id
                session['name'] = user.userName

                return redirect(url_for('tweets.tweet'))
            else:
                error = 'Invalid Username or Password'

    return render_template('index.html', form = form, error = error)


@users_routes.route('/register/', methods = ['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)

    if 'loggedIn' in session:
        return redirect(url_for('tweets.tweet'))

    if request.method == 'POST':
        if form.validate_on_submit():
            newUser = User(form.name.data, form.email.data, bcrypt.generate_password_hash(form.password.data).decode('utf-8'),)
            try:
                db.session.add(newUser)
                db.session.commit()

                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'Username and/or Email Already Exists'
                
                return render_template('register.html', form = form, error = error)

    return render_template('register.html', form = form, error = error)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'loggedIn' in session:
            return test(*args, **kwargs)
        else:
            return (redirect(url_for('users.login')))
    return wrap

@users_routes.route('/logout/')
@login_required
def logout():
    session.pop('loggedIn', None)
    session.pop('user_id', None)
    session.pop('name', None)

    return redirect(url_for('users.login'))

@users_routes.route('/users/')
@login_required
def all_users():
    users = db.session.query(User).all()

    return render_template('users.html', users = users)

@users_routes.route("/<username>")
@login_required
def profile(username):
    users = db.session.query(User).all()

    return render_template('users.html', users = users)


@users_routes.route('/users/follow/<int:user_id>/')
@login_required
def followUser(user_id):
    whomId = user_id
    try:
        whom = db.session.query(User).filter_by(id = whomId).first().userName

        if session['user_id'] != whomId:
            new_follow = Follower(session['user_id'], whomId)
            try:
                db.session.add(new_follow)
                db.session.commit()
                return redirect(url_for("users.profile", username = session['name']))
            except IntegrityError:
                return "## TODO ERROR ##"
        else:
            return redirect(url_for("users.profile", username = session['name']))
    except AttributeError:
        return "## TODO ERROR ##"

@users_routes.route('/users/unfollow/<int:user_id>/')
@login_required
def unfollowUser(user_id):
    whomId = user_id
    try:
        whom = db.session.query(User).filter_by(id = whomId).first().userName

        if session['user_id'] != whomId:
            following = db.session.query(Follower).filter_by(whoId = session['user_id'], whomId = whomId)

            if following.all():
                following.delete()
                db.session.commit()
                return redirect(url_for("users.profile", username = session['name']))
            else:
                return "## TODO ERROR ##"
        else:
            return redirect(url_for("users.profile", username = session['name']))
    except AttributeError:
        return "## TODO ERROR ##"