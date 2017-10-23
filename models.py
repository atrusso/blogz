from app import db
from datetime import datetime
from hashUtils import make_pw_hash, check_pw_hash

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_published = db.Column(db.DateTime)

    def __init__(self, title, body, owner, date_published=None):
        self.title = title
        self.body = body
        self.owner = owner
        if date_published is None:
            self.date_published = datetime.now()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    hash_password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.hash_password = make_pw_hash(password)