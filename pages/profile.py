import tkinter as tk
from tkinter import messagebox
from functions.session import Session
from database import users

class FrameProfile(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, width=1280, height=720, bg="#121212")
        self.controller = controller
        self.pack_propagate(False)

        # ----- NAVBAR -----
        navbar = tk.Frame(self, bg="#1E1E1E", height=50)
        navbar.pack(fill="x", side="top")

        # Título
        tk.Label(navbar, text="PopRate", font=("Helvetica", 20, "bold"), fg="#FFD700", bg="#1E1E1E").pack(side="left", padx=20)

        # Botón de volver (regresar a la página anterior)
        tk.Button(navbar, text="← Volver", font=("Helvetica", 12, "bold"),
                  bg="#FFD700", fg="#1E1E1E", activebackground="#FFC107",
                  command=self.volver).pack(side="right", padx=20)

        # ----- CONTENIDO PRINCIPAL -----
        content = tk.Frame(self, bg="#121212")
        content.pack(expand=True)

        user = Session.user or {}

        # Título principal
        tk.Label(content, text="Mi Perfil", font=("Helvetica", 24, "bold"),
                 fg="#FFD700", bg="#121212").pack(pady=(40, 20))

        # Campo: Nombre de usuario
        tk.Label(content, text="Nombre de usuario", font=("Helvetica", 14),
                 fg="#CCCCCC", bg="#121212").pack(anchor="w", padx=450)
        self.entry_username = tk.Entry(content, font=("Helvetica", 14),
                                       bg="#1E1E1E", fg="white", insertbackground="white",
                                       relief="flat", width=40)
        self.entry_username.insert(0, user.get("nombre_usuario", ""))
        self.entry_username.pack(pady=(5, 20))

        # Campo: Correo electrónico
        tk.Label(content, text="Correo electrónico", font=("Helvetica", 14),
                 fg="#CCCCCC", bg="#121212").pack(anchor="w", padx=450)
        self.entry_email = tk.Entry(content, font=("Helvetica", 14),
                                    bg="#1E1E1E", fg="white", insertbackground="white",
                                    relief="flat", width=40)
        self.entry_email.insert(0, user.get("correo_electronico", ""))
        self.entry_email.pack(pady=(5, 30))

        # Botón: Guardar datos
        btn_save = tk.Button(content, text="Guardar Datos",
                             font=("Helvetica", 12, "bold"),
                             bg="#FFD700", fg="#1E1E1E",
                             activebackground="#FFC107",
                             activeforeground="#1E1E1E",
                             command=self.guardar_datos)
        btn_save.pack(pady=(10, 20))

        # Botón: Cambiar contraseña
        btn_change_pass = tk.Button(content, text="Cambiar Contraseña",
                                    font=("Helvetica", 12, "bold"),
                                    bg="#FFD700", fg="#1E1E1E",
                                    activebackground="#FFC107",
                                    activeforeground="#1E1E1E",
                                    command=self.cambiar_contraseña)
        btn_change_pass.pack(pady=(10, 10))
    # ---- FUNCIONES ----

    def cambiar_contraseña(self):
        messagebox.showinfo("Cambiar contraseña", "Aquí se abriría una ventana para cambiar la contraseña.")

    def guardar_datos(self):
        nombre = self.entry_username.get()
        email = self.entry_email.get()
        result_update = users.update_user(nombre,email)
        
        if result_update == 0:
            messagebox.showwarning("Cambios Realizados", "Se realizaron los cambios correctamente")
            self.master.destroy()
        elif result_update == 1:
            messagebox.showwarning("Error desconocido", "Ocurrio un error inesperado")
        elif result_update == 2:
            messagebox.showwarning("Datos duplicados", "El usuario/email ya esta en usp")

        if not nombre or not email:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return


    def volver(self):
        if self.controller:
            self.controller.show_frame("FrameStartPage")
        else:
            self.master.destroy()

