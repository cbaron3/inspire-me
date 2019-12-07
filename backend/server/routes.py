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

from server.util import validNumber, validTime

# Add authentication
    # basic auth https://stackoverflow.com/questions/44072750/how-to-send-basic-auth-with-axios
    # python side https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
    # track users on server side on server
    # https://gist.github.com/miguelgrinberg/5614326

# Add twilio helper functions
#   subscribe is similar to POST except also sends a message using twilio. Check if number exists and validate both number and time
#   receive handles twilio webhook. also for checking if user confirms registration. also add easter eggs like perhaps suicide pervention hotline number and the such
    # similar to PUT request but modifies users CONFIRMED status
    # check if message comes from trusted source. if not, respond with URL 

# Then add background tasking

# Then deploy

# Plan is currenly to send the same quote to everyone; could have track which users received which quotes for variety. 
    # Everyday send different quotes to users

# Route not found
@app.errorhandler(404)
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def not_found_error(error):
    return jsonify({'error': '404', 'message': 'route not found'}), 404

# Interal Server error
@app.errorhandler(500)
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': '500', 'message': 'internal server error'}), 500

# Subscribers API:
#   Get all users (filters are optional)
#   Delete all users (filters are optional)
#   Add new user (filters required)
@app.route("/api/v1/resources/users", methods=['GET', 'POST', 'DELETE'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def allUsers():
    if request.method == 'GET':
        # Get all users
        try:
            number = request.args.get('phone_number')
            time = request.args.get('time')

            if number and not validNumber(number):
                return jsonify({'message': 'Invalid parameters; Phone number improperly formatted'}), 404

            if time and not validTime(time, '%H:%M'):
                return jsonify({'message': 'Invalid parameters; Time improperly formatted'}), 404

            if number and time:
                books = Subscriber.query.filter_by(number=number, time=time)
            elif number:
                books = Subscriber.query.filter_by(number=number)
            elif time:
                books = Subscriber.query.filter_by(time=time)
            else:
                books = Subscriber.query.all()

            return jsonify([e.serialize() for e in books]), 200
        except Exception as e:
            db.session.rollback()
            print('Exception when getting all users: {}'.format(str(e)))
            return jsonify({'message': 'Exception when getting all users'}), 404

    if request.method == 'DELETE':
        # Delete all users
        try:
            number = request.args.get('phone_number')
            time = request.args.get('time')
            
            if number and not validNumber(number):
                return jsonify({'message': 'Invalid parameters; Phone number improperly formatted'}), 404

            if time and not validTime(time, '%H:%M'):
                return jsonify({'message': 'Invalid parameters; Time improperly formatted'}), 404

            if number and time:
                deleted = Subscriber.query.filter_by(number=number, time=time).delete()
            elif number:
                deleted = Subscriber.query.filter_by(number=number).delete()
            elif time:
                deleted = Subscriber.query.filter_by(time=time).delete()
            else:
                deleted = Subscriber.query.delete()

            db.session.commit()
            return jsonify({'Deleted': deleted}), 200
        except Exception as e:
            db.session.rollback()
            print('Exception when deleting all users: {}'.format(str(e)))
            return jsonify({'message': 'Exception when deleting all users'}), 404

    if request.method == 'POST':
        try:
            number = request.args.get('phone_number')
            time = request.args.get('time')

            if number and not validNumber(number):
                return jsonify({'message': 'Invalid parameters; Phone number improperly formatted'}), 404

            if time and not validTime(time, '%H:%M'):
                return jsonify({'message': 'Invalid parameters; Time improperly formatted'}), 404

            if not number or not time:
                return jsonify({'message': 'Invalid parameters; Need both phone_number and time'}), 404
            else:
                has_number = Subscriber.query.filter_by(number=number).first()
                if has_number:
                    return jsonify({'message': 'There exists a user with that phone number'.format(id)}), 404
                else:
                    result = Subscriber(number=number, time=time)
                    db.session.add(result)
                    db.session.commit()
                    return "Subscriber added. Subscriber id={}".format(result.id)
        except Exception as e:
            db.session.rollback()
            print('Exception when adding new users: {}'.format(str(e)))
            return jsonify({'message': 'Exception when adding new users'}), 404

# Subscribers API
#   Get a user by ID (filters ignored)
#   Delete a user by ID (filters ignored)
#   Update a user by ID (need either parameter)
@app.route("/api/v1/resources/users/<int:id>", methods=['GET', 'PUT', 'DELETE'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def singleUser(id):
    if request.method == 'GET':
        # Get a single user by ID
        try:
            user = Subscriber.query.get(id)
            if user:
                return jsonify(user.serialize()), 200
            else:
                return jsonify({'message': 'User with ID {} does not exist'.format(id)}), 404
        except Exception as e:
            db.session.rollback()
            print('Exception when getting a user: {}'.format(str(e)))
            return jsonify({'message': 'Exception when getting a user by id'}), 404

    if request.method == 'DELETE':
        try:
            deleted = Subscriber.query.filter_by(id=id).delete()
            db.session.commit()
            if deleted:
                return jsonify({'message': 'User with ID {} deleted'.format(id)}), 200
            else:
                return jsonify({'message': 'User with ID {} does not exist'.format(id)}), 404
        except Exception as e:
            db.session.rollback()
            print('Exception when getting a user: {}'.format(str(e)))
            return jsonify({'message': 'Exception when deleting a user by id'}), 404

    if request.method == 'PUT':
        try:
            # Get user
            user = Subscriber.query.get(id)
            if not user:
                return jsonify({'message': 'User with ID {} does not exist'.format(id)}), 404

            # If number supplied, update the number if does not exist in the table
            number = request.args.get('phone_number')
            time = request.args.get('time')

            if number and not validNumber(number):
                return jsonify({'message': 'Invalid parameters; Phone number improperly formatted'}), 404

            if time and not validTime(time, '%H:%M'):
                return jsonify({'message': 'Invalid parameters; Time improperly formatted'}), 404

            if number:
                # TODO: Check if valid phone number!!!
                has_number = Subscriber.query.filter_by(number=number).first()
                if has_number:
                    return jsonify({'message': 'There exists a user with that phone number'.format(id)}), 404
                else:
                    user.number = number
    
            if time:
                user.time = time

            confirmed = request.args.get('confirmed')
            if confirmed:
                user.confirmed = confirmed

            db.session.commit()
            return jsonify(user.serialize()), 200

        except Exception as e:
            db.session.rollback()
            print('Exception when updating a user: {}'.format(str(e)))
            return jsonify({'message': 'Exception when updating a user by id'}), 404

# Quotes API:
#   Get all quotes (filters are optional)
#   Delete all quotes (filters are optional)
#   Add quote user (filters required)
@app.route("/api/v1/resources/quotes", methods=['GET', 'POST', 'DELETE'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def allQuotes():
    if request.method == 'GET':
        # Get all quotes; with filters if included
        try:
            quote = request.args.get('quote')
            quote_hash = request.args.get('quote_id')
            freq = request.args.get('frequency')

            # TODO: Ignoring filter by quote hash right now
            # Bad design, not easily maintained
            if quote and freq:
                quotes = Quote.query.filter_by(quote=quote, frequency=freq)
            elif freq:
                quotes = Quote.query.filter_by(frequency=freq)
            elif quote:
                quotes = Quote.query.filter_by(quote=quote)
            else:
                quotes = Quote.query.all()

            return jsonify([q.serialize() for q in quotes]), 200
        except Exception as e:
            db.session.rollback()
            print('Exception when getting all quotes: {}'.format(str(e)))
            return jsonify({'message': 'Exception when getting all quotes'}), 404

    if request.method == 'DELETE':
        # Delete all quotes; with filters if included
        try:
            quote = request.args.get('quote')
            quote_hash = request.args.get('quote_id')
            freq = request.args.get('frequency')

            # TODO: Ignoring filter by quote hash right now
            # Bad design, not easily maintained
            if quote and freq:
                quotes = Quote.query.filter_by(quote=quote, frequency=freq).delete()
            elif freq:
                quotes = Quote.query.filter_by(frequency=freq).delete()
            elif quote:
                quotes = Quote.query.filter_by(quote=quote).delete()
            else:
                quotes = Quote.query.delete()
            
            db.session.commit()
            return jsonify({'Deleted': quotes}), 200
        except Exception as e:
            db.session.rollback()
            print('Exception when deleting all quotes: {}'.format(str(e)))
            return jsonify({'message': 'Exception when deleting all quotes'}), 404

    if request.method == 'POST':
        try:
            quote = request.args.get('quote')
            quote_hash = request.args.get('quote_id')
            freq = request.args.get('frequency')

            if quote_hash:
                return jsonify({'message': 'Invalid parameters; Do not supply quote hash'}), 404
            
            # TODO: Check if quote already exists, if yes, do put
            # TODO: generate hash of string
            result = Quote(quote=quote, quote_hash=0)
            db.session.add(result)
            db.session.commit()
            return "Quote added. Quote id={}".format(result.id)

        except Exception as e:
            db.session.rollback()
            print('Exception when adding new quote: {}'.format(str(e)))
            return jsonify({'message': 'Exception when adding new quote'}), 404

# Quotes API
#   Get a quote by ID (filters ignored)
#   Delete a quote by ID (filters ignored)
#   Update a quote by ID (need at least parameter)
@app.route("/api/v1/resources/quotes/<int:id>", methods=['GET', 'PUT', 'DELETE'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def singleQuote(id):
    if request.method == 'GET':
        # Get a single quote by ID
        try:
            quote = Quote.query.get(id)
            if quote:
                return jsonify(user.serialize()), 200
            else:
                return jsonify({'message': 'Quote with ID {} does not exist'.format(id)}), 404
        except Exception as e:
            db.session.rollback()
            print('Exception when getting a quote: {}'.format(str(e)))
            return jsonify({'message': 'Exception when getting a quote by id'}), 404

    if request.method == 'DELETE':
        try:
            deleted = Quote.query.filter_by(id=id).delete()
            db.session.commit()
            if deleted:
                return jsonify({'message': 'Quote with ID {} deleted'.format(id)}), 200
            else:
                return jsonify({'message': 'Quote with ID {} does not exist'.format(id)}), 404
        except Exception as e:
            db.session.rollback()
            print('Exception when getting a quote: {}'.format(str(e)))
            return jsonify({'message': 'Exception when deleting a quote by id'}), 404

    if request.method == 'PUT':
        # Update, should only need to update frequency. Going to increase by 1
        try:
            quote = Quote.query.get(id)
            if quote:
                quote.frequency += 1
                db.session.commit()
                return jsonify(quote.serialize()), 200
            else:
                return jsonify({'message': 'Quote with ID {} does not exist'.format(id)}), 404
        except Exception as e:
            db.session.rollback()
            print('Exception when updating a quote: {}'.format(str(e)))
            return jsonify({'message': 'Exception when updating a quote by id'}), 404


@app.route("/api/v1/resources", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def allResources():
    try:

        users = Subscriber.query.all()
        quotes = Quote.query.all()

        result = {
            'users': [u.serialize() for u in users],
            'quotes': [q.serialize() for q in quotes]
        }

        return jsonify(result), 200

    except Exception as e:
            db.session.rollback()
            print('Exception when getting all resources: {}'.format(str(e)))
            return jsonify({'message': 'Exception when getting all resources'}), 404


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