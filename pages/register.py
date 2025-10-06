import tkinter as tk
from tkinter import messagebox
from database import register
import bcrypt

class FrameRegister(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")

        # Título
        label_titulo = tk.Label(self, text="Registro de Usuario", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=20)

        # Usuario
        label_usuario = tk.Label(self, text="Usuario", font=("Arial", 12), bg="#f0f0f0")
        label_usuario.pack(pady=(10,0))
        self.entry_usuario = tk.Entry(self, font=("Arial", 12))
        self.entry_usuario.pack(pady=5)

        # Correo
        label_correo = tk.Label(self, text="Correo", font=("Arial", 12), bg="#f0f0f0")
        label_correo.pack(pady=(10,0))
        self.entry_correo = tk.Entry(self, font=("Arial", 12))
        self.entry_correo.pack(pady=5)

        # Contraseña
        label_contraseña = tk.Label(self, text="Contraseña", font=("Arial", 12), bg="#f0f0f0")
        label_contraseña.pack(pady=(10,0))
        self.entry_contraseña = tk.Entry(self, font=("Arial", 12), show="*")
        self.entry_contraseña.pack(pady=5)

        # Confirmar contraseña
        label_confirm = tk.Label(self, text="Confirmar Contraseña", font=("Arial", 12), bg="#f0f0f0")
        label_confirm.pack(pady=(10,0))
        self.entry_confirm = tk.Entry(self, font=("Arial", 12), show="*")
        self.entry_confirm.pack(pady=5)

        # Botón registrar
        btn_registrar = tk.Button(self, text="Registrar", font=("Arial", 12, "bold"), bg="#2196f3", fg="white",
                                  activebackground="#1e88e5", padx=10, pady=5, command=self.registrar)
        btn_registrar.pack(pady=20)

        # Botón volver al login
        btn_login = tk.Button(self, text="Volver al Login", font=("Arial", 10), fg="#2196f3", bg="#f0f0f0",
                              activebackground="#e0e0e0", command=lambda: controller.mostrar_frame("FrameLogin"))
        btn_login.pack(pady=5)

    def registrar(self):
        usuario = self.entry_usuario.get()
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()
        confirm = self.entry_confirm.get()

        # Validaciones simples
        if not usuario or not correo or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if contraseña != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return



        ## process to submit to databse
        contraseña = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt())
        contraseña = contraseña.decode("utf-8")

        result = register.registrar(usuario,correo,contraseña)
        if result==-1:
            messagebox.showerror("Error", "El usuario o correo ya estan creados")
            return
        elif result ==-2:
            messagebox.showerror("Error", "Ocurrio un error en la peticion")
            return
        
        # Aquí podrías guardar los datos en una base de datos
        messagebox.showinfo("Registro", f"Usuario {usuario} registrado correctamente")


        # Limpiar campos
        self.entry_usuario.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_contraseña.delete(0, tk.END)
        self.entry_confirm.delete(0, tk.END)

        # Volver al login
        self.controller.mostrar_frame("FrameLogin")
