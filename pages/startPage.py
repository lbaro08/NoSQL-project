import tkinter as tk
from tkinter import ttk
from database import films
from pages.detailMovie import FrameDetailMovie
from pages.addMovie import FrameAddMovie
from pages.profile import FrameProfile
from functions.session import Session
from tkinter import messagebox
class FrameStartPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, width=1280, height=720)
        self.controller = controller
        self.configure(bg="#121212")
        self.pack_propagate(False)
        
        # ----- NAVBAR -----
        navbar = tk.Frame(self, bg="#1E1E1E", height=50)
        navbar.pack(fill="x", side="top")

        # Título PopRate
        tk.Label(navbar, text="PopRate", font=("Helvetica", 20, "bold"), fg="#FFD700", bg="#1E1E1E").pack(side="left", padx=20)

        # Botón Agregar película
        tk.Button(navbar, text="Agregar película", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=self.agregar_pelicula).pack(side="right", padx=(0,20))

        # Botón de cuenta
        tk.Button(navbar, text="Mi Cuenta", font=("Helvetica", 12, "bold"),
                  bg="#FFD700", fg="#1E1E1E", activebackground="#FFC107",
                  command=self.ver_cuenta).pack(side="right", padx=20)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(self, bg="#FFFB00", highlightthickness=0, width=1280, height=720)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#121212")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Ejemplo de datos de películas
        peliculas = films.get("mainPage")
        
        #*peliculas.add(           {
        #        "nombre": "Matrix22",
        #        "tipo": "Película",
        #        "sinopsis": "Un hacker descubre la realidad oculta detrás del mundo.",
        #        "año": 1999,
        #        "genero": "Ciencia ficción"
        #    })
 

        # Crear un frame por cada película
        for peli in peliculas:
            self._crear_card(peli)

    def _crear_card(self, data):
        card = tk.Frame(self.scrollable_frame, bg="#1e1e1e", bd=0, highlightthickness=0)
        card.pack(pady=15, padx=30, fill="x")

        # Título
        tk.Label(card, text=data['nombre'], font=("Helvetica", 18, "bold"), fg="#FFD700", bg="#1e1e1e").pack(anchor="w", padx=15, pady=(10,2))
        # Tipo y año
        tk.Label(card, text=f"{'Pelicula' if data['tipo'] == 1 else 'Serie'} | {data['año']}", font=("Helvetica", 12), fg="#CCCCCC", bg="#1e1e1e").pack(anchor="w", padx=15)
        # Género
        tk.Label(card, text=f"Género: {data['genero']}", font=("Helvetica", 12), fg="#CCCCCC", bg="#1e1e1e").pack(anchor="w", padx=15)
        # Sinopsis
        tk.Label(card, text=f"Sinopsis: {data['sinopsis']}", font=("Helvetica", 12), fg="#EEEEEE", bg="#1e1e1e", wraplength=1200, justify="left").pack(anchor="w", padx=15, pady=(5,10))

        # Botón "Ver más"
        btn = tk.Button(card, text="Ver más", font=("Helvetica", 12, "bold"), bg="#FFD700", fg="#1e1e1e",
                        activebackground="#FFC107", activeforeground="#1e1e1e",
                        command=lambda d=data: self.ver_mas(d))
        btn.pack(anchor="e", padx=15, pady=(0,10))

    def ver_mas(self, data):
        movie_id = str(data['_id'])
        print("Id de  ",movie_id)
        ventana_detalle = tk.Toplevel(self)
        ventana_detalle.geometry("1280x720")
        ventana_detalle.title(data['nombre'])
        ventana_detalle.configure(bg="#121212")

        detalle = FrameDetailMovie(ventana_detalle, movie_id=movie_id)
        detalle.pack(fill="both", expand=True)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # ---- Mostrar datos de la cuenta -----
    def ver_cuenta(self):
        
        ventana_my_profile = tk.Toplevel(self)
        ventana_my_profile.geometry("1280x720")
        ventana_my_profile.title("Mi perfil")
        ventana_my_profile.configure(bg="#121212")

        perfil = FrameProfile(ventana_my_profile)
        perfil.pack(fill="both", expand=True)

    def agregar_pelicula(self):
        ventana_add = tk.Toplevel(self)
        ventana_add.geometry("700x700")
        ventana_add.title("Agregar Película")
        ventana_add.configure(bg="#1E1E1E")
        frame_add = FrameAddMovie(ventana_add)
        frame_add.pack(fill="both", expand=True)
