# session.py
class Session:
    user = None

    @classmethod
    def login(cls, user_data):
        cls.user = user_data
        print("Entraron los datos a la sesion")
        print(cls.user.get("nombre_usuario"))
        print(user_data)

    @classmethod
    def logout(cls):
        cls.user = None

    @classmethod
    def is_logged_in(cls):
        return cls.user is not None
