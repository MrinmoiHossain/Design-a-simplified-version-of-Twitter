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

    @classmethod
    def is_following(cls, who_id, whom_id):
        whom_ids = db.session.query(Follower.whom_id).filter_by(who_id = who_id).all()
        whom_ids = [i[0] for i in whom_ids]
        
        if whom_id in whom_ids:
            return True
        else:
            return False

class Follower(db.Model):
    __tablename__ = 'follower'
    __table_args__ = (db.PrimaryKeyConstraint('who_id', 'whom_id'),)

    who_id = db.Column(db.Integer)
    whom_id = db.Column(db.Integer)

    def __init__(self, who_id, whom_id):
        self.who_id = who_id
        self.whom_id = whom_id