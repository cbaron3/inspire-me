# Flask
from flask import request
from flask_cors import cross_origin


from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client

# Secrets
from server.secrets import FROM_NUMBER, TO_NUMBER

from server import app, twilio_client

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

if __name__ == "__main__":
    app.run()