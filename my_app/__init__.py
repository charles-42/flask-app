from flask import Flask
from flask_login import LoginManager
from .models import init_db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

def create_app(mode = "development"):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    
    if mode  == "development":
        app.config.from_object('config.DevelopmentConfig')
    elif mode == "test":
        app.config.from_object('config.TestingConfig')
    elif mode == "production":
        app.config.from_object('config.ProductionConfig')

    #from my_app.models import db

    db = SQLAlchemy(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # since the id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(id))

    from my_app import models



    @app.cli.command("init_db")
    def init_db():
        models.init_db()


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

