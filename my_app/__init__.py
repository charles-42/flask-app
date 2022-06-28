import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_rbac import RBAC


app = Flask(__name__)
app.config.from_object('config')

# Create database connection object
db = SQLAlchemy(app)
#db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return models.User.query.get(int(user_id))

from my_app import models

# role base authorization configuration
rbac = RBAC(app)
rbac.set_role_model(models.Role)
rbac.set_user_model(models.User)






@app.cli.command("init_db")
def init_db():
    models.init_db()

from my_app import views

# # blueprint for auth routes in our app
# from .auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint)

# # blueprint for non-auth parts of app
# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)

