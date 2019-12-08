import os
from os.path import join, dirname

# Flask webserver import
from flask import Flask

# Cross origin requests handler
from flask_cors import CORS

# ORM for PSQL
from flask_sqlalchemy import SQLAlchemy

# Scheduler for background tasks
from flask_apscheduler import APScheduler

# Load dotenv files
from dotenv import load_dotenv
ENVDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(ENVDIR, '.env'))

# Load flask server with configuration settings
app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))

# Setup CORS
# TODO: Change from localhost and 5000 to env parameters for URL + PORT
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
# cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})

# Create ORM
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Scheduler for background tasks
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Add job to background tasks
# TODO: Change time interval for cron
from server.task import my_job
app.apscheduler.add_job(func=my_job, trigger='cron', second='*/5', id='1')

# Create twilio client
from twilio.rest import Client
from server.secrets import TWILIO_SID, TWILIO_AUTH
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Imports for linking
from server import routes