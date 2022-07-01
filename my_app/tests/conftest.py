from flask_sqlalchemy import SQLAlchemy
import pytest
from my_app import create_app, init_db


@pytest.fixture
def app():

    app = create_app('test')
    db = SQLAlchemy(app)

    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()


from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    chrome_driver = "/usr/local/bin/chromedriver"
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        yield driver
