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

print(os.environ.get('APP_SETTINGS'))
app.config.from_object(os.getenv('APP_SETTINGS'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})

db = SQLAlchemy(app)

# Create twilio client
from twilio.rest import Client
from server.secrets import TWILIO_SID, TWILIO_AUTH

twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Imports for linking
from server import routes