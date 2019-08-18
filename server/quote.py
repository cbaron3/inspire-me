import requests
import json

def inspiringQuote():
    # API url
    URL = 'http://quotes.rest/qod?category=inspire'

    # Get API response
    response = requests.get(URL)
    parsed = json.loads(response.text)

    # Return quote contents if API request was successful 
    if response.ok:
        print(parsed['contents']['quotes'][0]['quote'])
        print(parsed['contents']['quotes'][0]['length'])
        print(parsed['contents']['quotes'][0]['author'])
        print(parsed['contents']['quotes'][0]['date'])
    else:
        raise Exception('Error ' + str(parsed['error']['code']) + ' ' + parsed['error']['message'])

if __name__ == '__main__':
    try:
        inspiringQuote()
    except Exception as e:
        print(str(e))
    
    