import pymongo
from datetime import datetime
from decouple import config
import time
client = pymongo.MongoClient(config('MONGO_CLIENT'))
db = client[config('MONGO_DATABASE')]
collection = db['Variables']


def Token_Mongo_insert(token) -> None:
    x = datetime.today()
    date = x.strftime("%m/%d/%Y, %H:%M")
    post = {
        "_id": "IDGJ",
        "access_token": token['access_token'],
        "refresh_token": token['refresh_token'],
        "scope": token['scope'],
        "expires_in": time.time()+float(token['scope']),
        "refresh_token_expires_in": time.time()+float(token['refresh_token_expires_in']),
        "token_type": token['token_type']
    }
    collection.insert_one(post)
    print('\x1b[6;35;40m' + "Save Variable" + '\x1b[0m')


def Token_Mongo_find():
    results = collection.find_one({'_id': 'IDGJ'})
    print('\x1b[6;35;40m' + 'Mongo Data Got' + '\x1b[0m')
    return results


def Token_Mongo_delete() -> None:
    collection.delete_many({})


def token_Mongo_update(value):
    filter1 = {'_id': 'IDGJ'}
    newvalues = {"$set": value}
    collection.update_one(filter1, newvalues)
    print('Variable Update')
