import pymongo
from datetime import datetime
from decouple import config

client = pymongo.MongoClient(config("MONGO_CLIENT"))
db = client["Trading_Bote"]
collection = db['Pre_Lists']


def Prelist_Mongo_insert(lista, constant_band, market_cap, _id):
    x = datetime.today()
    date = x.strftime("%m/%d/%Y, %H:%M")
    post = {"_id": _id,
            "date": date,
            'list': lista,
            'constant_band': constant_band,
            'market_cap': market_cap
            }
    collection.insert_one(post)
    print('\x1b[6;35;40m' + "Save Prelist_Mongo" + '\x1b[0m')


def Prelist_Mongo_find(_id):
    results = collection.find_one({'_id': _id})
    print('\x1b[6;35;40m' + 'Mongo Data Got' + '\x1b[0m')
    return results


def Prelist_Mongo_last_data():
    result = collection.find().sort(
        '_id', pymongo.DESCENDING).limit(1)[0]
    return result
# collectio.delete_one({'_id':})
# collection.update_one({'_id:},{"$set":{"hello":}})
