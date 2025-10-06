from database import conection
import bcrypt
from datetime import datetime

def registrar(user,e_mail,password):

    collection = conection.conect('users')
    print("Entro a users\n")

    # verificamos is existe el user
    doc = collection.find_one({"$or": [{"nombre_usuario": user}, {"correo_electronico": e_mail}]})

    if doc:
        print("El usuario/correo ya esta registrado {user}\n")
        return -1
    
    try:
        collection.insert_one({
        "nombre_usuario": user,
        "correo_electronico":e_mail,
        "fecha_registro": datetime.now(),
        "password":password
        })
        return 1
    except Exception as ex:
        print("Ocurrio un error inesperado ",ex)
        return -2
    

