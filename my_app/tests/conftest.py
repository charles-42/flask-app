from flask_sqlalchemy import SQLAlchemy
import pytest
from my_app import create_app, init_db
from flask import template_rendered

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


# @pytest.fixture
# def driver():
#     chrome_driver = "/usr/local/bin/chromedriver"
#     with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
#         yield driver

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)