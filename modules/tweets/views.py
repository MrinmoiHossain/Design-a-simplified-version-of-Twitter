import datetime
from functools import wraps
from flask import redirect, render_template, request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from modules import db
from modules.models import Follower, Tweet
from .forms import PostTweetForm


tweets_routes = Blueprint('tweets', __name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'loggedIn' in session:
            return test(*args, **kwargs)
        else:
            return (redirect(url_for('users.login')))
    return wrap

def filtered_tweets(user_id):
    who_id = user_id
    whom_ids = db.session.query(Follower.whom_id).filter_by(who_id = who_id)
    user_tweets = db.session.query(Tweet).filter_by(userId = who_id)

    if whom_ids.all():
        follower_tweets = db.session.query(Tweet).filter(Tweet.userId.in_(whom_ids))
        result = user_tweets.union(follower_tweets)
        return result.order_by(Tweet.tweetTime.desc())
    else:
        return user_tweets.order_by(Tweet.tweetTime.desc())


@tweets_routes.route('/tweets/')
@login_required
def tweet():
    return render_template('tweets.html', form = PostTweetForm(), all_tweets = filtered_tweets(session['user_id']),)


@tweets_routes.route('/tweets/post/', methods=['GET', 'POST'])
@login_required
def post_tweet():
    error = None
    form = PostTweetForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_tweet = Tweet(form.tweet.data, datetime.datetime.now(), session['user_id'])
            db.session.add(new_tweet)
            db.session.commit()

            return redirect(url_for('tweets.tweet'))
    return render_template('tweets.html', form = form, error = error, all_tweets = filtered_tweets(session['user_id']),)


@tweets_routes.route('/tweets/delete/<int:tweetId>/')
@login_required
def delete_tweet(tweetId):
    our_tweetId = tweetId
    tweet = db.session.query(Tweet).filter_by(tweetId = our_tweetId)

    if tweet.first():
        if session['user_id'] == tweet.first().userId:
            tweet.delete()
            db.session.commit()
            return redirect(url_for('tweets.tweet'))
        else:
            return redirect(url_for('tweets.tweet'))
    else:
        return redirect(url_for('tweets.tweet'))
