from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    """
        Login form data validation class
        Data:
        - name
        - password
    """
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    """
        Registratioin form data validation class
        Data:
        - name
        - email
        - password
        - confirmPassword
    """
    name = StringField('Username', validators = [DataRequired(), Length(min = 6, max = 20)])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6, max = 32)])
    confirmPassword = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])

class PostTweetForm(FlaskForm):
    """
        Tweet post data validation class
        Data:
        - tweet
    """
    tweet = StringField('Tweet', validators=[DataRequired(), Length(min = 6, max = 120)])