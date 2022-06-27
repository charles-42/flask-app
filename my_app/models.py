from flask_sqlalchemy import SQLAlchemy
import logging as lg
from flask_login import UserMixin
from my_app import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))



def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(User(
        id = 1,
        email = "charles.beniac@gmail.com",
        pasword = "tobechanged",
        name = "Charles",
        ))
    db.session.commit()
    lg.warning('Database initialized!')