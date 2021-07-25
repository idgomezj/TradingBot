import pymongo
from datetime import datetime
from decouple import config

client = pymongo.MongoClient(config("MONGO_CLIENT"))
db = client["Trading_Bote"]
collection2 = db['Select']


def Select_Mongo_insert(select, _id, id_process, final_data):
    x = datetime.today()
    date = x.strftime("%m/%d/%Y, %H:%M")
    post = {"id_prelist": _id,
            "id_process": id_process,
            "date": date,
            "select": select,
            "final_data": final_data
            }
    collection2.insert_one(post)
    print('\x1b[6;35;40m' + "Save Select_Mongo" + '\x1b[0m')


def Select_Mongo_find(_id):
    results = collection2.find_one({"id_process": _id})
    print('\x1b[6;35;40m' + 'Mongo Data Got' + '\x1b[0m')
    return results


def Select_Mongo_last_data():
    result = collection2.find().sort(
        '_id', pymongo.DESCENDING).limit(1)[26]
    return result
# collectio.delete_one({'_id':})
# collection.update_one({'_id:},{"$set":{"hello":}})
