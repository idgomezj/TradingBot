import pandas as pd
import requests
import json
from decouple import config

def book_IexCloud(symbol):
    api_key = config("IEXCLOUD_KEY")
    base_URL = 'https://cloud.iexapis.com/'
    version = 'stable/'
    endpoint_path = 'deep/book'
    query_string = '?symbols=' + symbol + '&token='+api_key
    name = base_URL+version+endpoint_path+query_string
    response = requests.get(name)
    jsondata = response.json()
    return jsondata
