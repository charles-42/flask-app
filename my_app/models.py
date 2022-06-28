from flask_sqlalchemy import SQLAlchemy
import logging as lg
from flask_login import UserMixin
from my_app import db



class User(UserMixin,db.Model):


    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    group = db.Column(db.Integer)


    def __repr__(self):
        return f'{self.id} {self.name}, {self.group}'

    def json(self):
        return {
            'id': self.id, 
            'email_address': self.email_address,
            'name': self.name,
            'group': self.group
            }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()



def init_db():
    db.drop_all()
    db.create_all()
    

    
    first_user = User(
        id = 1,
        email = "cb@gmail.com",
        password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f',
        name = "Charles",
        group = 0 # 0 mean admin
        )
    first_user.save_to_db()
    
    second_user = User(
        id = 2,
        email = "tv@gmail.com",
        password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f',
        name = "Tony",
        group = 1 # 1 mean user
        )
    second_user.save_to_db()

    lg.warning('Database initialized!')