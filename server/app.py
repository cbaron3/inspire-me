from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# Subcribe route
@app.route('/subscribe', methods=['POST'])
def subscribe():
    params = request.args.to_dict()

    try:
        print( params['number'] )
        return 'Success', 200
    except:
        # If input parameters does not have term 'number', return Bad Request erro
        return 'Failure', 400
    
# Receive route
@app.route('/receive', methods=['POST'])
def receive():
    params = request.args.to_dict()

    try:
        print( params['number'] )
        print( params['content'] )
        return 'Success', 200
    except:
        # If input parameters does not have term 'number' and/or 'content', return Bad Request error
        return 'Failure', 400
        

if __name__ == '__main__':
    app.run()