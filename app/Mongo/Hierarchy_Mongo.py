import pymongo
from datetime import datetime
from decouple import config

client = pymongo.MongoClient(config("MONGO_CLIENT"))
db = client["Trading_Bote"]
collection1 = db['Hierarchy']


def Hierarchy_Mongo_insert(select, _id, id_process, final_data, json_book_data):
    x = datetime.today()
    date = x.strftime("%m/%d/%Y, %H:%M")
    post = {"id_prelist": _id,
            "id_process": id_process,
            "date": date,
            "select": select,
            'final_data': final_data,
            'json_book_data': json_book_data
            }
    collection1.insert_one(post)
    print('\x1b[6;35;40m' + "Save Hierarchy_Mongo" + '\x1b[0m')


def Hierarchy_Mongo_find(_id):
    results = collection1.find_one({'_id': _id})
    print('\x1b[6;35;40m' + 'Mongo Data Got' + '\x1b[0m')
    return results


def Hierarchy_Mongo_last_data():
    result = collection1.find().sort(
        '_id', pymongo.DESCENDING).limit(1)[0]
    return result
# collectio.delete_one({'_id':})
# collection.update_one({'_id:},{"$set":{"hello":}})
