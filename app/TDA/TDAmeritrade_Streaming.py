import asyncio
import json
import urllib
import requests
import dateutil.parser
from datetime import datetime
from .TDAmeritrade import get_acceess_token


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt-epoch).total_seconds()*1000.0


def tda_open():
    global userPrincipalsResponse
    global uri
    global login_encoded
    access_token = get_acceess_token()
    access_token = access_token['access_token']
    endpoint = 'https://api.tdameritrade.com/v1/userprincipals'
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    params = {'fields': 'streamerSubscriptionKeys,streamerConnectionInfo'}
    content = requests.get(url=endpoint, params=params, headers=headers)
    userPrincipalsResponse = content.json()
    # we need to get the timestamp in order to make our next request, but it needs to be parsed
    tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']
    date = dateutil.parser.parse(tokenTimeStamp, ignoretz=True)
    tokenTimeStampAsMs = unix_time_millis(date)
    # we need to define our credentials that we will need to make our stream
    credentials = {"userid": userPrincipalsResponse['accounts'][0]['accountId'],
                   "token": userPrincipalsResponse['streamerInfo']['token'],
                   "company": userPrincipalsResponse['accounts'][0]['company'],
                   "segment": userPrincipalsResponse['accounts'][0]['segment'],
                   "cddomain": userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
                   "usergroup": userPrincipalsResponse['streamerInfo']['userGroup'],
                   "accesslevel": userPrincipalsResponse['streamerInfo']['accessLevel'],
                   "authorized": "Y",
                   "timestamp": int(tokenTimeStampAsMs),
                   "appid": userPrincipalsResponse['streamerInfo']['appId'],
                   "acl": userPrincipalsResponse['streamerInfo']['acl']}
    # define a request
    login_request = {"requests": [{"service": "ADMIN",
                                   "requestid": "0",
                                   "command": "LOGIN",
                                   "account": userPrincipalsResponse['accounts'][0]['accountId'],
                                   "source": userPrincipalsResponse['streamerInfo']['appId'],
                                   "parameters": {"credential": urllib.parse.urlencode(credentials),
                                                  "token": userPrincipalsResponse['streamerInfo']['token'],
                                                  "version": "1.0"}}]}
    login_encoded = json.dumps(login_request)
    uri = "wss://" + \
        userPrincipalsResponse['streamerInfo']['streamerSocketUrl'] + "/ws"


async def websocketconnect(data_encoded):
    async with websockets.connect(uri) as ws:
        await ws.send(login_encoded)
        await ws.send(data_encoded)
        cycle = True
        while cycle:
            received = await ws.recv()
            json_data = json.loads(received)
            if 'data' in json_data:
                return json_data


def book_data(symbol):
    tda_open()
    data_request = {
        "requests": [
            {
                "service": "NASDAQ_BOOK",
                "requestid": "2",
                "command": "SUBS",
                "account": userPrincipalsResponse['accounts'][0]['accountId'],
                "source": userPrincipalsResponse['streamerInfo']['appId'],
                "parameters": {
                    "keys": symbol,
                    "fields": "0,1,2,3,4,5,6,7,8"
                }
            }
        ]
    }
    data_encoded = json.dumps(data_request)
    return asyncio.get_event_loop().run_until_complete(websocketconnect(data_encoded))


def active_nasdaq():
    tda_open()
    data_request = {
        "requests": [
            {
                "service": "ACTIVES_NASDAQ",
                "requestid": "3",
                "command": "SUBS",
                "account": userPrincipalsResponse['accounts'][0]['accountId'],
                "source": userPrincipalsResponse['streamerInfo']['appId'],
                "parameters": {
                    "keys": "NASDAQ-60",
                    "fields": "0,1"
                }
            }]}
    data_encoded = json.dumps(data_request)
    return asyncio.get_event_loop().run_until_complete(websocketconnect(data_encoded))
