from pymongo import MongoClient


def conect(name_collection):
    try:
        client = MongoClient('localhost',27017)
        database = client["meview"]
        collection=database[name_collection]
        return collection
        
    except Exception as ex:
        print("Ocurrion un error :" , ex )
        

