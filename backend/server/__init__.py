# Create flask server
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})

# Create twilio client
from twilio.rest import Client
from server.secrets import TWILIO_SID, TWILIO_AUTH

twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Imports for linking
from server import routes