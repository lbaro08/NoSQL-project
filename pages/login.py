import tkinter as tk
from tkinter import messagebox
import bcrypt
from functions.session import Session

## improt base de datos
from database import login

class FrameLogin(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f5f5f5")
        self.controller = controller

        # Contenedor central
        container = tk.Frame(self, bg="white", bd=2, relief="groove")
        container.grid(row=0, column=0, sticky="nsew")  # Ocupa toda la celda
        self.rowconfigure(0, weight=1)   # Hace que la fila crezca
        self.columnconfigure(0, weight=1)  # Hace que la columna crezca

        # Título
        label_titulo = tk.Label(container, text="Iniciar Sesión", font=("Helvetica", 20, "bold"), bg="white", fg="#333333")
        label_titulo.pack(pady=(20, 30))

        # Usuario
        tk.Label(container, text="Usuario", font=("Helvetica", 12), bg="white", fg="#555555").pack(pady=(10,5))
        self.entry_usuario = tk.Entry(container, font=("Helvetica", 12), bd=2, relief="groove")
        self.entry_usuario.pack(pady=5, ipady=5, ipadx=5, padx=40)

        # Contraseña
        tk.Label(container, text="Contraseña", font=("Helvetica", 12), bg="white", fg="#555555").pack(pady=(15,5))
        self.entry_contraseña = tk.Entry(container, font=("Helvetica", 12), show="*", bd=2, relief="groove")
        self.entry_contraseña.pack(pady=5, ipady=5, ipadx=5, padx=40)

        # Botón login
        tk.Button(container, text="Ingresar", font=("Helvetica", 12, "bold"),
                  bg="#4caf50", fg="white", activebackground="#45a049",
                  activeforeground="white", command=self.login).pack(pady=(30,10), ipadx=10, ipady=5)

        # Botón registro
        tk.Button(container, text="Registrarse", font=("Helvetica", 12, "underline"),
                  bg="#393A39", fg="#ffffff", bd=0,
                  activebackground="white", activeforeground="#1976d2",
                  command=lambda: controller.mostrar_frame("FrameRegister")).pack(pady=(5,20))

        # Footer opcional
        tk.Label(container, text="© 2025 PopRate", font=("Helvetica", 9), bg="white", fg="#999999").pack(side="bottom", pady=10)

    def login(self):
        usuario = self.entry_usuario.get()
        #parseo de contrasena
        contraseña = self.entry_contraseña.get()
        contraseña = contraseña.encode("utf-8")        
        check = login.logear(usuario,contraseña)

        if check:
            Session.login(check)
            messagebox.showinfo("Login", "¡Bienvenido!") 
            if self.controller: 
                self.controller.mostrar_frame("FrameStartPage")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        


    
