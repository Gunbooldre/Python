from flask_login import UserMixin
from datetime import datetime

from application import db,manager

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow())
    
    def __init__(self,fullname,age):
        self.fullname = fullname
        self.age = age

class Login(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow())
    
    def __init__(self,username,password):
        self.username = username
        self.password = password

@manager.user_loader
def load_user(user):
    return Login.query.get(user) #== select * from Login where id = user

