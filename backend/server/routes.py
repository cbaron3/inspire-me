# Flask
from flask import request, jsonify
from flask_cors import cross_origin


from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client

# Secrets
from server.secrets import FROM_NUMBER, TO_NUMBER

from server import app, twilio_client, db
from server.models import Subscriber, Quote

# HTTP Actions
    # Get
        # Get resource
            # Get all used quotes
            # Get single used quote
            # Get all users
            # Get user
    # Post
        # Add user
        # Add quote to tracked table
    # Put
        # Update user status
    # Delete
        # Delete user
        # Delete quote from tracked quotes
    # Patch
        # Partial update to resource

# Add config and dev ops settings
# Add database
    # postgres
# Add all rest methods
# Add authentication
    # basic auth https://stackoverflow.com/questions/44072750/how-to-send-basic-auth-with-axios
    # python side https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
    # track users on server side on server
    # https://gist.github.com/miguelgrinberg/5614326
# Subscribe route
@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    params = request.get_json()

    # If we are supplied a valid number, send subscription message

    try:
        number = params['number']

        # Check here for valid with algorithm
        valid = True

        if valid:
            # Start background task that adds subscriber to table and sends welcome message
            return 'Success', 200
        else:
            return 'Failure', 400
    except Exception as e:
        print(str(e))
        return 'Failure', 400


@app.route('/sms/test', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def frontend():
    number = request.get_json()
    print(number['number'])

    message = twilio_client.messages.create(
        #to=number['number'], 
        to=TO_NUMBER,
        from_=FROM_NUMBER,
        body="Thank you for enrolling, please reply CONFIRMED to confirm")

    return "Success"


@app.route('/sms/receive', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    print(message_body)

    resp = MessagingResponse()
    if message_body == 'CONFIRMED':
        resp.message('Entry confirmed')
    else:
        resp.message('Entry denied')
    
    return str(resp)


@app.errorhandler(404)
def not_found_error(error):
    return 'Error', 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return 'Error', 500

# ************* USERS ************* #

# Get all users, delete all users
@app.route("/api/v1/resources/users", methods=['GET', 'DELETE'])
def allUsers():
    if request.method == 'GET':
        try:
            books = Subscriber.query.all()
            return jsonify([e.serialize() for e in books])
        except Exception as e:
            db.session.rollback()
            return(str(e))
    elif request.method == 'DELETE':
        try:
            books = Subscriber.query.delete()
            db.session.commit()
            return "All users deleted"
        except Exception as e:
            db.session.rollback()
            return(str(e))
    else:
        # Invalid method, return error
        return "All users invalid method", 404

# Get a user, delete a user
@app.route("/api/v1/resources/users/<int:id>", methods=['GET', 'DELETE'])
def singleUser(id):
    # Single user by ID
    if request.method == 'GET':
        try:
            user = Subscriber.query.get(id)
            return jsonify(user.serialize())
        except Exception as e:
            db.session.rollback()
            return(str(e))
    elif request.method == 'DELETE':
        try:
            user = Subscriber.query.filter_by(id=id).delete()
            print(user)
            db.session.commit()
            if user:
                return 'Deleted user'
            else:
                return 'User does not exist'
        except Exception as e:
            db.session.rollback()
            return(str(e))
        pass
    else:
        # Invalid method, return error
        pass

# Update user by ID
@app.route("/api/v1/resources/users/<int:id>/", methods=['PUT'])
def updateUser(id):
    # Update user by add
    pass


# Create user with filters. Check if user with number exists
@app.route("/api/v1/resources/users/", methods=['GET', 'POST'])
def newUsers():
    # Create user; similar to subscribe method tho...supply phone number and time
    pass


# Dummy user for testing
@app.route("/api/v1/resources/users/dummy", methods=['GET', 'POST'])
def dummyUser():
    try:
        result = Subscriber(number='123-456-7890', time='12:00')
        db.session.add(result)
        db.session.commit()
        return "Subscriber added. Subscriber id={}".format(result.id)
    except Exception as e:
        db.session.rollback()
        return(str(e))
















# ************* QUOTES ************* #
# Get all quotes
@app.route("/api/v1/resources/quotes/all", methods=['GET', 'DELETE'])
def allQuotes():
    if request.method == 'GET':
        try:
            books = Quote.query.all()
            return jsonify([e.serialize() for e in books])
        except Exception as e:
            db.session.rollback()
            return(str(e))
    elif request.method == 'DELETE':
        try:
            books = Quote.query.delete()
            db.session.commit()
            return "All quotes deleted"
        except Exception as e:
            db.session.rollback()
            return(str(e))
    else:
        # Invalid method, return error
        return "All users invalid method", 404

# Get a quotes, delete a quotes, update a user
@app.route("/api/v1/resources/quotes/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def singleQuote():
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        # Invalid method, return error
        pass

# Get quotes with filters
# Add a new quotes with parameters
# Delete a quotes based on parameters
@app.route("/api/v1/resources/quotes", methods=['GET', 'POST', 'DELETE'])
def filteredQuotes():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        # Invalid method, return error
        pass
