import urllib
from selenium import webdriver
import time
from decouple import config
import requests
from Mongo import *
from authlib.integrations.httpx_client import OAuth2Client


def get_historical_candles(symbol: str):
    endpoint = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory"
    payload = {'apikey': config('API_KEY'),
               'periodType': 'day',
               'frequencyType': 'minute',
               'frequency': '1',
               'period': '2',
               'endDate': int(time.time()*1000),
               # 'starDate': '1554535854000',
               'needExtendedHoursData': 'true'}
    content = requests.get(url=endpoint, params=payload)
    data = content.json()
    return data


def update_token(refresh_token):
    url = r'https://api.tdameritrade.com/v1/oauth2/token'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {'grant_type': 'refresh_token',
               'refresh_token': refresh_token,
               'client_id': config('API_KEY')}
    authReply = requests.post(url, headers=headers, data=payload)
    decoded_content = authReply.json()
    #access_token = decoded_content['access_token'].split('==', 1)[0]
    result = {'access_token': decoded_content['access_token']}
    token_Mongo_update({**result,
                        'expires_in': time.time()+1800})
    return result


def get_refresh_token(refresh_token):
    url = r'https://api.tdameritrade.com/v1/oauth2/token'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {'grant_type': 'refresh_token',
               'refresh_token': refresh_token,
               'access_type': 'offline',
               'client_id': config('API_KEY')}
    authReply = requests.post(url, headers=headers, data=payload)
    decoded_content = authReply.json()
    decoded_content['expires_in'] = decoded_content['expires_in']+time.time()
    decoded_content['refresh_token_expires_in'] = decoded_content['refresh_token_expires_in']+time.time()
    token_Mongo_update(decoded_content)
    return decoded_content


def get_token():
    method = 'GET'
    redirect_url = 'https://localhost'
    url = 'https://auth.tdameritrade.com/auth?'
    client_code = config('API_KEY')
    oauth = OAuth2Client(client_code, redirect_uri=redirect_url)
    authorization_url, state = oauth.create_authorization_url(
        'https://auth.tdameritrade.com/auth')
    with webdriver.Chrome(executable_path=config('CHROMEDRIVER_PATH')) as driver:
        driver.get(authorization_url)
        if redirect_url.startswith('http://'):
            print(('WARNING: Your redirect URL ({}) will transmit data over HTTP, ' +
                   'which is a potentially severe security vulnerability. ' +
                   'Please go to your app\'s configuration with TDAmeritrade ' +
                   'and update your redirect URL to begin with \'https\' ' +
                   'to stop seeing this message.').format(redirect_url))

            redirect_urls = (redirect_url, 'https' + redirect_url[4:])
        else:
            redirect_urls = (redirect_url,)

        current_url = ''
        num_waits = 0
        max_waits = 100000
        while not any(current_url.startswith(r_url) for r_url in redirect_urls):
            current_url = driver.current_url
            if num_waits > max_waits:
                print('Wait Login Error')
            time.sleep(0.1)
            num_waits += 1

    parse_url = urllib.parse.unquote(current_url.split('code=')[1])
    parse_url = parse_url.split('&', 1)[0]

    url = r'https://api.tdameritrade.com/v1/oauth2/token'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {'grant_type': 'authorization_code',
               'refresh_token': '',
               'access_type': 'offline',
               'code': parse_url,
               'client_id': config('API_KEY')+'@AMER.OAUTHAP',
               'redirect_uri': config('REDIRECT_URI')}
    authReply = requests.post(url, headers=headers, data=payload)
    decoded_content = authReply.json()
    Token_Mongo_insert(decoded_content)
    return decoded_content


def get_acceess_token():
    token = Token_Mongo_find()
    if token == None:
        token = get_token()
    else:
        if token['refresh_token_expires_in'] < time.time():
            token = get_refresh_token(token['refresh_token'])
        elif token['expires_in'] < time.time():
            token = update_token(token['refresh_token'])
    return {'access_token': token['access_token']}


def get_account():
    access_token = get_acceess_token()
    access_token = access_token['access_token']
    headers = {'Authorization': "Bearer {}".format(access_token)}
    accountId = config('ACCOUNT_ID')
    endpoint = f"https://api.tdameritrade.com/v1/accounts/{accountId}"
    content = requests.get(url=endpoint, headers=headers)
    data = content.json()
    return data

