from database import conection
import bcrypt
from bson.objectid import ObjectId
from pymongo import DESCENDING


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
    elif operacion == 'mostValoratedFilmOpc':
        collection = conection.conect('films_full_details')
        resultado = collection.find_one(
            {"tipo": 1},
            sort=[("promedio_calificacion", DESCENDING), ("total_reseñas", DESCENDING)]
        )
        return resultado

    elif operacion == 'mostValoratedSerieOpc':
        collection = conection.conect('films_full_details')
        resultado = collection.find_one(
            {"tipo": 0},
            sort=[("promedio_calificacion", DESCENDING), ("total_reseñas", DESCENDING)]
        )
        return resultado



def put(data):
    collection = conection.conect('films')
    
    result = collection.insert_one(data)
    print(f"🎬 Película/Serie agregada: {data['titulo']}, ID: {result.inserted_id}")
    return str(result.inserted_id)
    

