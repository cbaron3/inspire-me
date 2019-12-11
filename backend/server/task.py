from server import twilio_client
from server.models import Subscriber, Quote

from server.secrets import FROM_NUMBER

from server.quote import getQuote

def my_job():
    users = Subscriber.query.all()

    quote = getQuote()
    quote = quote['quote'] + ' - ' + quote['author']
    for user in users:
        message = twilio_client.messages.create(
            #to=number['number'], 
            to=user.number,
            from_=FROM_NUMBER,
            body=quote)
        print('Text sent to: {}'.format(user.number))
