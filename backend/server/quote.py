import requests
import json

def getQuote():
    # TODO: Need to credit source for project --> https://quotes.rest/#!/qod/get_qod
    URL = 'http://quotes.rest/qod?category=inspire'

    # Get API response
    response = requests.get(URL)
    parsed = json.loads(response.text)

    # Return quote contents if API request was successful 
    if response.ok:
        result = {
            'quote': parsed['contents']['quotes'][0]['quote'],
            'author': parsed['contents']['quotes'][0]['author']
        }

        return result
    else:
        raise Exception('Error ' + str(parsed['error']['code']) + ' ' + parsed['error']['message'])
        return None
    
    

if __name__ == '__main__':
    try:
        print(getQuote())
    except Exception as e:
        print(str(e))
