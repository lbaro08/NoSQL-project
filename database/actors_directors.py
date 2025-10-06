from database import conection
import bcrypt

def get(type = None):
    collection = conection.conect('actors_directors')
    if type == 'directors':
        return collection.find({"tipo": 1})
    elif type == 'actors':
        return collection.find({"tipo": 0})
    else:
        return collection.find()
