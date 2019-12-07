# Create flask server
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname
from dotenv import load_dotenv
ENVDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(ENVDIR, '.env'))


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

app.config.from_object(os.getenv('APP_SETTINGS'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})

db = SQLAlchemy(app)


from flask_apscheduler import APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from server.task import my_job
print(app.apscheduler.get_jobs())
# https://apscheduler.readthedocs.io/en/v2.1.2/cronschedule.html
app.apscheduler.add_job(func=my_job, trigger='cron', second='*/5', id='1') # trigger every 5 seconds. (every time seconds ends with 5)

# Create twilio client
from twilio.rest import Client
from server.secrets import TWILIO_SID, TWILIO_AUTH

twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Imports for linking
from server import routes