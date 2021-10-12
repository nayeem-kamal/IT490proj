from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint 
import os

pp = pprint.PrettyPrinter(indent=4)

url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
print(url)
key = "092f78e5-80ec-4b38-8d06-c6b8b9d9d852"
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': key,
}
parameters = {
'id':'1,2,3,4'

}

session = Session()
session.headers.update(headers)
try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    pp.pprint(data)
    

except (ConnectionError, Timeout, TooManyRedirects) as e:
    data = json.loads(response.text)
    pp.pprint(data)
