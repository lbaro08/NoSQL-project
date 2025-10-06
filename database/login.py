from database import conection
import bcrypt

def logear(input,password):

    collection = conection.conect('users')
    print("Entro a users\n")

    # verificamos is existe el user
    doc = collection.find_one({"$or": [{"nombre_usuario": input}, {"correo_electronico": input}]})
    if not doc:
        print("No se encontro al usuario {input}\n")
        return False
    
    # if it exists, we get its password
    password_stored = doc.get("password")

    # password is converted on bytes
    if isinstance(password_stored, str):
        password_stored = password_stored.encode("utf-8")

    
    if bcrypt.checkpw(password, password_stored):
        print("Contraseña correcta")
        return doc
    else:
        print("Contraseña incorrecta")
        return False