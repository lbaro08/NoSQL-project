from database import conection
import bcrypt
from bson.objectid import ObjectId

def get(operacion,id = None):
    
    print("Entro a Films\n")

    if operacion == "mainPage":
        collection = conection.conect('main_page_films')
        docs = collection.find()
        resultados = list(docs)
        return resultados
    
    elif operacion == 'filmDetailsOpc':
        collection = conection.conect('films_full_details')
        print("jejejej")
        doc = collection.find_one({"_id":ObjectId(id)})
        resultado = doc
        return resultado



def put(data):
    collection = conection.conect('films')
    
    result = collection.insert_one(data)
    print(f"🎬 Película/Serie agregada: {data['titulo']}, ID: {result.inserted_id}")
    return str(result.inserted_id)
    

