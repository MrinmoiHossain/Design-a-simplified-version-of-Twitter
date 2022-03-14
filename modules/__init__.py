import os
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# Get the application secret key and Database URL from the environment variable
SECRET_KEY = str(os.environ.get('SECRET_KEY'))
DATABASE_URI = str(os.environ.get('DATABASE_URI'))

# Initialize the Flask Application
app = Flask(__name__)

# Set application configuration environment
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database ORM
db = SQLAlchemy(app)

# Initialize the password hashing library
bcrypt = Bcrypt(app)

# Application routing module call
from modules import routes

# Creating database schemas
db.create_all()
db.session.commit()