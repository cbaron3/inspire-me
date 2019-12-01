# Flask
from flask import Flask, request
from flask_cors import CORS, cross_origin
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client

# Secrets
import secrets

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})

@app.route('/sms/test', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def frontend():
    number = request.get_json()
    print(number['number'])

    client = Client(secrets.TWILIO_SID, secrets.TWILIO_AUTH)

    message = client.messages.create(
        #to=number['number'], 
        to=secrets.TO_NUMBER,
        from_=secrets.FROM_NUMBER,
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