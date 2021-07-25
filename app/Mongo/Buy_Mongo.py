import pymongo
from datetime import datetime
from decouple import config

client = pymongo.MongoClient(config("MONGO_CLIENT"))
db = client["Trading_Bote"]
collection2 = db['Buy']


def Buy_Mongo_insert(stop_lost_order, buy_order, qty, information, stop_lost_information, _id, id_process):
    x = datetime.today()
    date = x.strftime("%m/%d/%Y, %H:%M")
    post = {"id_prelist": _id,
            "id_process": id_process,
            "date": date,
            "buy_order": buy_order,
            "stop_lost_order": stop_lost_order,
            'qty': qty,
            'information': information,
            'stop_lost_information': stop_lost_information,
            'qty_remnant': qty
            }
    collection2.insert_one(post)
    print('\x1b[6;35;40m' + "Save Buy_Mongo" + '\x1b[0m')


def Buy_Mongo_find(_id):
    results = collection2.find_one({'_id': _id})
    print('\x1b[6;35;40m' + 'Mongo Data Got' + '\x1b[0m')
    return results


def Buy_Mongo_last_data():
    result = collection2.find().sort(
        '_id', pymongo.DESCENDING).limit(1)[0]
    return result
# collectio.delete_one({'_id':})
# collection.update_one({'_id:},{"$set":{"hello":}})


def Buy_Mongo_update(value, id_process):
    filter1 = {'id_process': id_process}
    newvalues = {"$set": {'qty_remnant': value}}
    collection2.update_one(filter1, newvalues)
