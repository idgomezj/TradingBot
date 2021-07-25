import pymongo
from datetime import datetime
from decouple import config

client = pymongo.MongoClient(config("MONGO_CLIENT"))
db = client["Trading_Bote"]
collection3 = db['Sell']


def Sell_Mongo_insert(sell_order, qty, information,  _id, id_process):
    x = datetime.today()
    date = x.strftime("%m/%d/%Y, %H:%M")
    post = {"id_prelist": _id,
            "id_process": id_process,
            "date": date,
            "sell_order": sell_order,
            "qty": qty,
            'information': information
            }
    collection3.insert_one(post)
    print('\x1b[6;35;40m' + "Save Sell_Mongo" + '\x1b[0m')


def Sell_Mongo_find(_id):
    results = collection3.find_one({'_id': _id})
    print('\x1b[6;35;40m' + 'Mongo Data Got' + '\x1b[0m')
    return results


def Sell_Mongo_last_data():
    result = collection3.find().sort(
        '_id', pymongo.DESCENDING).limit(1)[0]
    return result
# collectio.delete_one({'_id':})
# collection.update_one({'_id:},{"$set":{"hello":}})
