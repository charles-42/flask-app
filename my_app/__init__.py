from flask import Flask
from flask_login import LoginManager
from .models import init_db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace import config_integration
from opencensus.ext.azure import metrics_exporter

import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

def create_app(mode = "development"):
    
    # Upload env variables
    load_dotenv()
    print("this is the instrument key ----------------------------------")
    print(os.getenv('CONNEXION_STRING'))
    # Create APP
    app = Flask(__name__, instance_relative_config=True)
    
    # Select config
    if mode  == "development":
        app.config.from_object('config.DevelopmentConfig')
    elif mode == "test":
        app.config.from_object('config.TestingConfig')
    elif mode == "production":
        app.config.from_object('config.ProductionConfig')


    # Connect to DB
    db = SQLAlchemy(app)

    # Connoct to log manager with flask login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # since the id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(id))


    # Define cli command to initiate DB
    from my_app import models

    @app.cli.command("init_db")
    def init_db():
        models.init_db()

    # Define routes
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Define monitoring
    middleware = FlaskMiddleware(app)
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(
    connection_string = os.getenv('CONNEXION_STRING'))
    )
    logger.setLevel(logging.INFO)
    config_integration.trace_integrations(['sqlalchemy'])

    exporter = metrics_exporter.new_metrics_exporter(
        enable_standard_metrics=False,
        connection_string=os.getenv('CONNEXION_STRING'))


    # OPentelemetry

    exporter = AzureMonitorTraceExporter.from_connection_string(os.getenv('CONNEXION_STRING'))

    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    span_processor = BatchSpanProcessor(exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    FlaskInstrumentor().instrument_app(app)


    return app

