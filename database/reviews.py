from database import conection
import bcrypt
from bson.objectid import ObjectId

def putReview(user_id,movie_id,review_data = None):

    collection = conection.conect('reviews')
    
    user_id = ObjectId(user_id)   # ejemplo
    movie_id = ObjectId(movie_id)  # "El Padrino"

    existe_review = collection.find_one({
        "id_usuario": user_id,
        "id_pelicula_serie": movie_id
    })

    if existe_review:
        print("Ya existe una reseña:", existe_review)
        return 1
    else:
        try:
            collection.insert_one({
                "id_usuario":review_data["id_usuario"],
                "id_pelicula_serie":review_data["id_pelicula_serie"],
                "calificacion":review_data["calificacion"],
                "texto_reseña":review_data["texto_reseña"],
                "fecha_publicacion":review_data["fecha_publicacion"],
                "votos_utilidad":review_data["votos_utilidad"]

            })
            return 0
        except Exception as ex:
            print("Ocurrio un error inesperado ",ex)
            return 2
    