from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Task(UserMixin, db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    started = db.Column(db.String)
    finished = db.Column(db.String)
    status = db.Column(db.String)
    step = db.Column(db.Integer)
    file_path = db.Column(db.String)
    result = db.Column(db.String)

    def __init__(self, name, started, finished, status, step, file_path, result):
        self.name = name
        self.started = started
        self.finished = finished
        self.status = status
        self.step = step
        self.file_path = file_path
        self.result = result

    def __repr__(self):
        return '<Task %r>' % self.id

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    gender = db.Column(db.String)
    register_date = db.Column(db.String)

    def __init__(self, firstname, lastname, username, email, password, gender, register_date):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.register_date = register_date

    def __repr__(self):
        return '<User %r>' % self.username

class Login(UserMixin, db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    password = db.Column(db.String(256))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, authenticated):
        self.username = username
        self.password = password
        self.authenticated = authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<Login %r>' % self.username