from server import db

# Subscriber table. Used to store users who have subscribed to the service
class Subscribers(db.Model):
    __tablename__ = 'subscribers'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    # Phone number of user
    number = db.Column(db.String())
    # Time that the user wishes to be notified at. TODO: This will be a later feature after I get scheduled tasks to work
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

# Quotes table. Used to store quotes that have been sent out
class Quotes(db.Model):
    __tablename__ = 'quotes'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    # Quote string
    quote = db.Column(db.String())
    # Quote hash to reduce comparison complexity between quotes (I think)
    quote_hash = db.Column(db.Integer())
    
    def __init__(self, quote, quote_hash):
        self.quote = quote
        self.quote_hash = quote_hash

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'quote': self.quote,
            'quote_hash': self.quote_hash
        }

