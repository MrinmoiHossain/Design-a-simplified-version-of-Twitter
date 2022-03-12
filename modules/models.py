from modules import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(32), nullable = False)

    def __init__(self, userName = None, email = email, password = None):
        self.userName = userName
        self.email = email
        self.password = password