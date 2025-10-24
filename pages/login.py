import tkinter as tk
from tkinter import messagebox
import bcrypt
from functions.session import Session
from database import login

class FrameLogin(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        # Contenedor central
        container = tk.Frame(self, bg="#1E1E1E", bd=0, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center")  # Centrado absoluto
        container.config(width=400, height=400)
        
        # Título
        label_titulo = tk.Label(container, text="Iniciar Sesión", font=("Helvetica", 22, "bold"),
                                bg="#1E1E1E", fg="#FFD700")
        label_titulo.pack(pady=(30, 30))

        # Usuario
        tk.Label(container, text="Usuario", font=("Helvetica", 12), bg="#1E1E1E", fg="#CCCCCC").pack(anchor="w", padx=40, pady=(10,2))
        self.entry_usuario = tk.Entry(container, font=("Helvetica", 12), bg="#2C2C2C", fg="white",
                                      bd=0, relief="flat", insertbackground="white")
        self.entry_usuario.pack(pady=(0,10), ipady=8, ipadx=10, padx=40)

        # Contraseña
        tk.Label(container, text="Contraseña", font=("Helvetica", 12), bg="#1E1E1E", fg="#CCCCCC").pack(anchor="w", padx=40, pady=(10,2))
        self.entry_contraseña = tk.Entry(container, font=("Helvetica", 12), show="*", bg="#2C2C2C", fg="white",
                                        bd=0, relief="flat", insertbackground="white")
        self.entry_contraseña.pack(pady=(0,20), ipady=8, ipadx=10, padx=40)

        # Botón login
        tk.Button(container, text="Ingresar", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#45a049",
                  activeforeground="white", bd=0, relief="flat",
                  command=self.login).pack(pady=(10,15), ipadx=10, ipady=8)

        # Botón registro
        tk.Button(container, text="Registrarse", font=("Helvetica", 11, "underline"),
                  bg="#1E1E1E", fg="#FFD700", bd=0, relief="flat",
                  activebackground="#1E1E1E", activeforeground="#FFC107",
                  command=lambda: controller.mostrar_frame("FrameRegister")).pack(pady=(5,20))

        # Footer opcional
        tk.Label(container, text="© 2025 PopRate", font=("Helvetica", 9), bg="#1E1E1E", fg="#777777").pack(side="bottom", pady=10)

    def login(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        contraseña = contraseña.encode("utf-8")        
        check = login.logear(usuario, contraseña)

        if check:
            Session.login(check)
            messagebox.showinfo("Login", "¡Bienvenido!") 
            if self.controller: 
                self.controller.mostrar_frame("FrameStartPage")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
