from twilio.rest import Client
import os

if __name__ == "__main__":
    # Your Account SID from twilio.com/console
    account_sid = os.environ.get('TWILIO_SID')
    # Your Auth Token from twilio.com/console
    auth_token  = os.environ.get('TWILIO_TOKEN')

    number = os.environ.get('TWILIO_NUMBER')
    my_number = os.environ.get('MY_NUMBER')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=my_number, 
        from_= number,
        body="Hello from Python!")

    print(message.sid)