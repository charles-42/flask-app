from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os, sys, inspect
from .. import app
from .. import models
from ..models import User, init_db

# Third party modules
import pytest

# First party modules
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config.from_object('my_app.tests.config')
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # A partir de celui-ci je déduis le chemin de mon répertoire parent
    parentdir = os.path.dirname(currentdir)
    grandparentdir = os.path.dirname(parentdir)
    template_folder_path = os.path.join(grandparentdir, "/tests/templates")
    app.template_folder = template_folder_path
    db = SQLAlchemy(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
    # since the id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(id))


    # blueprint for auth routes in our app
    from ..auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, template_folder = template_folder_path)

    # blueprint for non-auth parts of app
    from ..main import main as main_blueprint
    app.register_blueprint(main_blueprint, template_folder = template_folder_path)

    client = app.test_client()

    with app.app_context():
        # init_db()
        db.drop_all()
        db.create_all()
        
        # first_user = User(
        #     id = 1,
        #     email = "cb@gmail.com",
        #     password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f',
        #     name = "Charles",
        #     group = 0 # 0 mean admin
        #     )
        # first_user.save_to_db()
        
        # second_user = User(
        #     id = 2,
        #     email = "tv@gmail.com",
        #     password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f',
        #     name = "Tony",
        #     group = 1 # 1 mean user
        #     )
        # second_user.save_to_db()

        
    yield client



@pytest.fixture
def driver():
    chrome_driver = "/usr/local/bin/chromedriver"
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        yield driver


def test_easy(client):
    route = "/"
    rv = client.get(route)
    assert rv.status_code == 200



# def test_user_login(client,driver):
    
#     # On ouvre le navigateur avec l'adresse du serveur.
#     driver.get("https://www.google.com")
#     # L'adresse dans l'url doit être celle que l'on attend.
#     assert driver.current_url == 'https://www.google.com/'