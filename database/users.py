from database import conection
import bcrypt
from datetime import datetime
from functions.session import Session
collection = conection.conect('users')

def update_user(new_username,new_email):  

    doc = collection.find_one({"$or": [{"nombre_usuario": new_username}, {"correo_electronico": new_email}]})

    if doc.get("_id")!=Session.user.get("_id"):
        print("El usuario/correo ya esta registrado {user}\n")
        return 2
    else:
    
        try:
            collection.update_one(
                {"_id": Session.user.get("_id")},
                {"$set": {
                    "nombre_usuario": new_username,
                    "correo_electronico": new_email,
                }})
            
            user = collection.find_one({"_id": Session.user.get("_id")})
            Session.login(user)

            return 0
        except:
            print("Error")
            return 1