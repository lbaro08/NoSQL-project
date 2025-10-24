import tkinter as tk
from tkinter import messagebox
from database import register
import bcrypt

class FrameRegister(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        # Contenedor central
        container = tk.Frame(self, bg="#1E1E1E", bd=0, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.config(width=450, height=500)

        # Título
        label_titulo = tk.Label(container, text="Registro de Usuario", font=("Helvetica", 22, "bold"),
                                bg="#1E1E1E", fg="#FFD700")
        label_titulo.pack(pady=(30, 30))

        # Usuario
        tk.Label(container, text="Usuario", font=("Helvetica", 12), bg="#1E1E1E", fg="#CCCCCC").pack(anchor="w", padx=40, pady=(5,2))
        self.entry_usuario = tk.Entry(container, font=("Helvetica", 12), bg="#2C2C2C", fg="white",
                                      bd=0, relief="flat", insertbackground="white")
        self.entry_usuario.pack(pady=(0,10), ipady=8, ipadx=10, padx=40)

        # Correo
        tk.Label(container, text="Correo", font=("Helvetica", 12), bg="#1E1E1E", fg="#CCCCCC").pack(anchor="w", padx=40, pady=(5,2))
        self.entry_correo = tk.Entry(container, font=("Helvetica", 12), bg="#2C2C2C", fg="white",
                                     bd=0, relief="flat", insertbackground="white")
        self.entry_correo.pack(pady=(0,10), ipady=8, ipadx=10, padx=40)

        # Contraseña
        tk.Label(container, text="Contraseña", font=("Helvetica", 12), bg="#1E1E1E", fg="#CCCCCC").pack(anchor="w", padx=40, pady=(5,2))
        self.entry_contraseña = tk.Entry(container, font=("Helvetica", 12), show="*", bg="#2C2C2C", fg="white",
                                        bd=0, relief="flat", insertbackground="white")
        self.entry_contraseña.pack(pady=(0,10), ipady=8, ipadx=10, padx=40)

        # Confirmar contraseña
        tk.Label(container, text="Confirmar Contraseña", font=("Helvetica", 12), bg="#1E1E1E", fg="#CCCCCC").pack(anchor="w", padx=40, pady=(5,2))
        self.entry_confirm = tk.Entry(container, font=("Helvetica", 12), show="*", bg="#2C2C2C", fg="white",
                                      bd=0, relief="flat", insertbackground="white")
        self.entry_confirm.pack(pady=(0,20), ipady=8, ipadx=10, padx=40)

        # Botón registrar
        btn_registrar = tk.Button(container, text="Registrar", font=("Helvetica", 12, "bold"),
                                  bg="#3E8E41", fg="white", bd=0, relief="flat",
                                  activebackground="#45a049", activeforeground="white",
                                  command=self.registrar)
        btn_registrar.pack(pady=(10,15), ipadx=10, ipady=8)

        # Botón volver al login
        btn_login = tk.Button(container, text="Volver al Login", font=("Helvetica", 11, "underline"),
                              bg="#1E1E1E", fg="#FFD700", bd=0, relief="flat",
                              activebackground="#1E1E1E", activeforeground="#FFC107",
                              command=lambda: controller.mostrar_frame("FrameLogin"))
        btn_login.pack(pady=5)

        # Footer
        tk.Label(container, text="© 2025 PopRate", font=("Helvetica", 9), bg="#1E1E1E", fg="#777777").pack(side="bottom", pady=10)

    def registrar(self):
        usuario = self.entry_usuario.get()
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()
        confirm = self.entry_confirm.get()

        # Validaciones
        if not usuario or not correo or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if contraseña != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        # Encriptar contraseña
        contraseña = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        result = register.registrar(usuario, correo, contraseña)
        if result == -1:
            messagebox.showerror("Error", "El usuario o correo ya están registrados")
            return
        elif result == -2:
            messagebox.showerror("Error", "Ocurrió un error en la petición")
            return

        messagebox.showinfo("Registro", f"Usuario {usuario} registrado correctamente")

        # Limpiar campos
        self.entry_usuario.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_contraseña.delete(0, tk.END)
        self.entry_confirm.delete(0, tk.END)

        # Volver al login
        self.controller.mostrar_frame("FrameLogin")
