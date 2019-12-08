from server import db
from sqlalchemy import DateTime

# Messages received from users
class Received(db.Model):
    __tablename__ = 'received'

    # Track
        # ID, primary key
        # Number, number that sent the message
        # Recv_msg, message contents that was received
        # Sent_msg, message that was sent by backend as response
        
    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Number that sent us the message
    number = db.Column(db.String())

    # The received message
    recv_msg = db.Column(db.String())

    # The sent response
    sent_msg = db.Column(db.String())

    def __init__(self, number, received, sent):
        self.number = number
        self.recv_msg = received
        self.sent_msg = sent

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'number': self.number,
            'recv_msg': self.recv_msg,
            'sent_msg': self.sent_msg
        }

# People subscribing to the inspire me service
class Subscriber(db.Model):
    # Table name will be subscribers
    __tablename__ = 'subscribers'

    # Track 
    #   ID, primary key
    #   number, number to send/receive SMS to
    #   confirmed, status of if user is confirmed or not
    #   time, track what time of day the user wants their message
        # just unsubscribe to change time?

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

# Track which quotes are sent out.
# Perhaps track with quotes users received for variety
class Quote(db.Model):
    # Tablename will be quotes
    __tablename__ = 'quotes'

    # Track
    #   ID, primary key
    #   quote, string containing the actual quote
    #   quote_hash, hash for simpler comparison
    #   frequency, check how much it was used

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