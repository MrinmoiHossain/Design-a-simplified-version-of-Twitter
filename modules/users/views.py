import datetime
from functools import wraps
from flask import Blueprint, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

# Database related modules import
from modules import db, bcrypt
from modules.models import User, Follower, Tweet

from .forms import RegisterForm, LoginForm, PostTweetForm

# Main blueprint, name as users
users_routes = Blueprint('users', __name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'loggedIn' in session:
            return test(*args, **kwargs)
        else:
            return (redirect(url_for('users.login')))
    return wrap

def filteredTweets(user_id):
    """
        Filter the tweets from the database using user id number.
        Input: user_id
        Oupute: List of tweets descending order 
    """

    whoId = user_id
    whomIds = db.session.query(Follower.whomId).filter_by(whoId = whoId)
    userTweets = db.session.query(Tweet).filter_by(userId = whoId)

    if whomIds.all():
        follower_tweets = db.session.query(Tweet).filter(Tweet.userId.in_(whomIds))
        result = userTweets.union(follower_tweets)
        return result.order_by(Tweet.tweetTime.desc())
    else:
        return userTweets.order_by(Tweet.tweetTime.desc())


@users_routes.route('/home/', methods = ['GET', 'POST'])
@login_required
def homePage():
    """
        User homepage routing path.
        Accept Method: GET, POST
    """

    return render_template('home.html', form = PostTweetForm(), allTweets = filteredTweets(session['user_id']))


@users_routes.route('/', methods = ['GET', 'POST'])
@users_routes.route('/login', methods = ['GET', 'POST'])
def login():
    """
        User login page
        Accept Method: GET, POST
    """

    error = None
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(userName = request.form['name']).first()

            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                session['loggedIn'] = True
                session['user_id'] = user.id
                session['name'] = user.userName

                return redirect(url_for('users.homePage'))
            else:
                error = 'Invalid Username or Password'

    return render_template('index.html', form = form, error = error)


@users_routes.route('/register/', methods = ['GET', 'POST'])
def register():
    """
        User registration page
        Accept Method: GET, POST
    """

    error = None
    form = RegisterForm(request.form)

    if 'loggedIn' in session:
        return redirect(url_for("users.homePage"))

    if request.method == 'POST':
        if form.validate_on_submit():
            newUser = User(form.name.data, form.email.data, bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
            try:
                db.session.add(newUser)
                db.session.commit()

                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'Username and/or Email Already Exists'
                
                return render_template('register.html', form = form, error = error)

    return render_template('register.html', form = form, error = error)


@users_routes.route('/users/', methods = ['GET'])
@login_required
def all_users():
    """
        User data page
        Accept Method: GET, POST
    """

    users = db.session.query(User).all()

    return render_template('users.html', users = users)


@users_routes.route("/<username>", methods = ['GET', 'POST'])
@login_required
def profile(username):
    """
        User profile
        Accept Method: GET, POST
    """

    error = None
    users = db.session.query(User).all()

    return render_template('profile.html', form = PostTweetForm(), error = error,  allTweets = filteredTweets(session['user_id']), users = users)


@users_routes.route('/<username>/tweets', methods = ['GET', 'POST'])
@login_required
def postTweet(username):
    """
        User tweets page
        Accept Method: GET, POST
    """

    error = None
    form = PostTweetForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_tweet = Tweet(form.tweet.data, datetime.datetime.now(), session['user_id'])
            db.session.add(new_tweet)
            db.session.commit()

            return redirect(request.url)
    return redirect(url_for("users.homePage"))


@users_routes.route('/<username>/tweets/delete/<int:tweetId>/', methods = ['GET', 'POST'])
@login_required
def deleteTweet(username, tweetId):
    """
        Delete the tweets for a user
        Accept Method: GET, POST
    """

    our_tweetId = tweetId
    tweet = db.session.query(Tweet).filter_by(tweetId = our_tweetId)

    if tweet.first():
        if session['user_id'] == tweet.first().userId:
            tweet.delete()
            db.session.commit()
            return redirect(url_for("users.profile", username = session['name']))
        else:
            return redirect(url_for("users.profile", username = session['name']))
    else:
        return redirect(url_for("users.profile", username = session['name']))


@users_routes.route('/users/follow/<int:user_id>/', methods = ['GET', 'POST'])
@login_required
def followUser(user_id):
    """
        Follow other users
        Accept Method: GET, POST
    """

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


@users_routes.route('/users/unfollow/<int:user_id>/', methods = ['GET', 'POST'])
@login_required
def unfollowUser(user_id):
    """
        Unfollow other users
        Accept Method: GET, POST
    """

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


@users_routes.route('/logout/', methods = ['GET', 'POST'])
@login_required
def logout():
    """
        Routing to the application logout page
        Input: None
        Ouput: redirect to user login page
    """
    session.pop('loggedIn', None)
    session.pop('user_id', None)
    session.pop('name', None)

    return redirect(url_for('users.login'))