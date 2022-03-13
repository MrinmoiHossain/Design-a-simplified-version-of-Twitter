import os
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

SECRET_KEY = str(os.environ.get('SECRET_KEY'))
DATABASE_URI = str(os.environ.get('DATABASE_URI'))

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from modules import routes

db.create_all()
db.session.commit()