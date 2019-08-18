import config
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# App instantiation
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from server import routes