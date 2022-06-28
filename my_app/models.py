from flask_sqlalchemy import SQLAlchemy
import logging as lg
from flask_login import UserMixin
from flask_rbac import RoleMixin
from my_app import db

from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin



roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    parents = db.relationship(
        'Role',
        secondary=roles_parents,
        primaryjoin=(id == roles_parents.c.role_id),
        secondaryjoin=(id == roles_parents.c.parent_id),
        backref=db.backref('children', lazy='dynamic')
    )

    def __init__(self, name):
        RoleMixin.__init__(self)
        self.name = name

    def __repr__(self):
        return f'{self.id} {self.name}'

    def add_parent(self, parent):
        # You don't need to add this role to parent's children set,
        # relationship between roles would do this work automatically
        self.parents.append(parent)

    def add_parents(self, *parents):
        for parent in parents:
            self.add_parent(parent)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_name(name):
        return Role.query.filter_by(name=name).first()
    

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(UserMixin,db.Model):


    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    roles = db.relationship(
        'Role',
        secondary=users_roles,
        backref=db.backref('roles', lazy='dynamic')
    )


    def __repr__(self):
        return f'{self.id} {self.name}, {self.get_roles_list()}'

    def json(self):
        return {
            'id': self.id, 
            'email_address': self.email_address,
            'name': self.name
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

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def get_roles(self):
        for role in self.roles:
            yield role
    
    def get_roles_list(self):
        role_list= []
        for role in self.roles:
            role_list.append(role.name)
        return role_list


def init_db():
    db.drop_all()
    db.create_all()
    
    admin = Role("admin")
    admin.save_to_db()
    
    first_user = User(
        id = 1,
        email = "cb@gmail.com",
        password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f',
        name = "Charles"
        )
    first_user.add_role(admin)
    first_user.save_to_db()
    
    second_user = User(
        id = 2,
        email = "tv@gmail.com",
        password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f',
        name = "Tony"
        )
    second_user.add_role(admin)
    second_user.save_to_db()

    lg.warning('Database initialized!')