# Flask API Template

This project is a web app built with Python and Flask to be used as a starter template.

## Virtualenv

python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt

## Auth and settings

create file in server named secrets.py
FROM_NUMBER = ""
TWILIO_SID = ""
TWILIO_AUTH = ""

## Testing with twilio

Use ngrok, ./ngrok http 5000 to generate a temporary url
My ngrok is in downloads
use that ngrok generate link and save it in your phone numbers. far left bar

## Built With

* [Python 3](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Docker](https://www.docker.com/)

## Prerequisites

You will need the following things properly installed on your computer:

* [Git](http://git-scm.com/)
* [Python 3](https://www.python.org/)
* [Docker](https://www.docker.com/)

## Installation

* run `git clone https://github.com/caseyr003/flask-react-template.git`

## Running

To run the project locally follow the following steps:

* change into the project directory
* `docker build -t backend-api .`
* `docker run -p 5000:5000 -v /HOST/PATH/TO/BACKEND/FOLDER:/app backend-api`

## JSON API

The JSON API is a test endpoint to start development

* `http://localhost:5000/api/test`
(returns a test json response)

## License

This project is licensed under the MIT License
