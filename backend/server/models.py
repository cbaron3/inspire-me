# Setting up PostgreSQL database along with SQLAlchemy and Alembic

# Create database db -- inspire

from server import db
from sqlalchemy import DateTime

class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    # ID, NUMBER, SUBSCRIBED, TIME OF DAY


    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Phone number of user
    number = db.Column(db.String())
    
    # Got store time as string
    time = db.Column(db.String())
    
    # Track whether the user has confirmed the user of the service
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, number, time=''):
        self.number = number
        self.time = time
        self.confirmed = False

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'number': self.number,
            'time': self.time,
            'confirmed': str(self.confirmed)
        }
        
class Quote(db.Model):
    __tablename__ = 'quotes'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    # Quote string
    quote = db.Column(db.String())
    # Quote hash to reduce comparison complexity between quotes (I think)
    quote_hash = db.Column(db.Integer())
    # frequency
    frequency = db.Column(db.Integer())
    
    def __init__(self, quote, quote_hash):
        self.quote = quote
        self.quote_hash = quote_hash
        self.frequency = 1

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'quote': self.quote,
            'quote_hash': self.quote_hash,
            'frequency': self.frequency
        }