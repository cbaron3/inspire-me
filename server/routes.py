from flask import Flask, jsonify, request
import os
from server import app, db
import re

from server.models import Subscribers, Quotes

def validNumber(number):
    # NOTE: Check for better options like better regex or phonenumbers lib
    pattern1 = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
    pattern2 = re.compile("^[\dA-Z]{3}[\dA-Z]{3}[\dA-Z]{4}$", re.IGNORECASE)
    return (pattern1.match(number) is not None) or (pattern2.match(number) is not None)

# Subcribe route
# TODO: I think I need to add headers or something here so that people can just post to my backend
@app.route('/subscribe', methods=['POST'])
def subscribe():
    params = request.args.to_dict()

    # If supplied and valid, send subscription confirmation text and add to unconfirmed table
        # TODO instead of waiting till after twillo sends and db is updated for return 200, just schedule
        # a background job instead on success and return 200
    
    try:
        # TODO: Need to also validate phone number on front end
        valid = validNumber(params['number'])

        if valid:
            # TODO: Schedule background task. If background task can fail, then need to update the 200/400 handling
            try:
                subscriber = Subscribers.query.filter_by(number=params['number']).first()
                if not subscriber:
                    result = Subscribers(number=params['number'], time="12:00:00")
                    db.session.add(result)
                    db.session.commit()
                    print("User added. User id={}".format(result.id))
                else:
                    print("User already exists")
            except Exception as e:
                print(str(e))

            return 'Success', 200
        else:
            # Input number is not valid
            return 'Failure', 400
    except Exception as e:
        # If input parameters does not have term 'number', return Bad Request error
        print(str(e))
        return 'Failure', 400
    
# Receive route
@app.route('/receive', methods=['POST'])
def receive():
    params = request.args.to_dict()

    try:
        valid = validNumber(params['number'])
        print(params['content'])

        if valid:
            # TODO: Schedule background task. If background task can fail, then need to update the 200/400 handling
            # Background task here takes in number/content and checks to see if need to confirm subscription, delete subscription, or handle untracked phone number
            # query
            try:
                user = Subscribers.query.filter_by(number=params['number']).first()
                if user and (params['content'] == 'YES' or params['content'] == 'yes'):
                    user.confirmed = True
                    db.session.commit()
                else:
                    print("Not a valid user")
            except Exception as e:
                print(str(e))
            
            return 'Success', 200
        else:
            # Input number is not valid
            return 'Failure', 400
    except Exception as e:
        # If input parameters does not have term 'number' and/or 'content', return Bad Request error
        print(str(e))
        return 'Failure', 400
        
# Database debugging routes
# add user
@app.route('/new_user', methods=['GET'])
def addUser():
    try:
        # Check if phone number already exists
        subscriber = Subscribers.query.filter_by(number="1234567890").first()
        if not subscriber:
            result = Subscribers(number="1234567890", time="12:00:00")
            db.session.add(result)
            db.session.commit()
            return "User added. User id={}".format(result.id)
        else:
            return "User already exists"
    except Exception as e:
        return(str(e))

@app.route("/all_users", methods=['GET'])
def allUsers():
    try:
        results=Subscribers.query.all()
        return  jsonify([e.serialize() for e in results])
    except Exception as e:
	    return(str(e))

@app.route("/delete_users", methods=['GET'])
def deleteUsers():
    try:
        results = Subscribers.query.delete()
        print(results)
        db.session.commit()
        return "Deleted users"
    except Exception as e:
        return(str(e))

@app.route("/new_quote", methods=['GET'])
def addQuote():
    try:
        result = Quotes(quote="To be or not to be", quote_hash=1234)
        db.session.add(result)
        db.session.commit()
        return "Quote added. Quote id={}".format(result.id)
    except Exception as e:
        return(str(e))

@app.route("/all_quotes", methods=['GET'])
def allQuotes():
    try:
        results = Quotes.query.all()
        return  jsonify([e.serialize() for e in results])
    except Exception as e:
	    return(str(e))

@app.route("/delete_quotes", methods=['GET'])
def deleteQuotes():
    try:
        results = Quotes.query.delete()
        print(results)
        db.session.commit()
        return "Deleted quotes"
    except Exception as e:
        return(str(e))