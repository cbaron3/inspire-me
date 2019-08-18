from server import db

class Subscribers(db.Model):
    __tablename__ = 'subscribers'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    time = db.Column(db.String())
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

class Quotes(db.Model):
    __tablename__ = 'quotes'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String())
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

