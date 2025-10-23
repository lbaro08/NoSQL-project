import tkinter as tk
from tkinter import ttk, messagebox
from database import films
from pages.detailMovie import FrameDetailMovie
from pages.addMovie import FrameAddMovie
from pages.profile import FrameProfile
from pages.actors_directors import FrameActors
from functions.session import Session


class FrameStartPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, width=1280, height=720)
        self.controller = controller
        self.configure(bg="#121212")
        self.pack_propagate(False)

        # ----- NAVBAR -----
        navbar = tk.Frame(self, bg="#1E1E1E", height=50)
        navbar.pack(fill="x", side="top")

        tk.Label(navbar, text="PopRate", font=("Helvetica", 20, "bold"),
                 fg="#FFD700", bg="#1E1E1E").pack(side="left", padx=20)

        tk.Button(navbar, text="Recargar 🔄", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=self.recargar_pagina).pack(side="left", padx=(10, 0))

        tk.Button(navbar, text="Agregar película", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=self.agregar_pelicula).pack(side="right", padx=(0, 20))

        tk.Button(navbar, text="Mi Cuenta", font=("Helvetica", 12, "bold"),
                  bg="#FFD700", fg="#1E1E1E", activebackground="#FFC107",
                  command=self.ver_cuenta).pack(side="right", padx=20)

        tk.Button(navbar, text="Actores", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=self.ver_actores).pack(side="right", padx=20)

        tk.Button(navbar, text="Directores", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=self.ver_directores).pack(side="right", padx=20)

        # ----- CONTENEDOR PRINCIPAL -----
        content_frame = tk.Frame(self, bg="#121212")
        content_frame.pack(fill="both", expand=True)

        # ----- IZQUIERDA: Canvas con películas -----
        left_frame = tk.Frame(content_frame, bg="#121212")
        left_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(left_frame, bg="#121212", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.canvas.yview)
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

        # ----- DERECHA: FILTROS -----
        right_frame = tk.Frame(content_frame, bg="#FFFB00", width=300)
        right_frame.pack(side="right", fill="y")

        tk.Label(right_frame, text="🎬 Filtros", bg="#FFFB00", fg="black",
                 font=("Helvetica", 16, "bold")).pack(pady=15)

        # --- Filtro por género ---
        # --- Filtro por género ---
        tk.Label(right_frame, text="Género:", bg="#FFFB00", fg="black",
                 font=("Helvetica", 12)).pack(anchor="w", padx=15)

        # Obtener géneros dinámicamente desde films
        peliculas = films.get("mainPage")
        generos_unicos = set()

        for peli in peliculas:
            genero = peli.get("genero", [])
            if isinstance(genero, list):
                generos_unicos.update(genero)
            elif isinstance(genero, str):
                generos_unicos.add(genero)

        generos_ordenados = sorted(list(generos_unicos))
        opciones_genero = ["Todos"] + generos_ordenados

        # Crear combobox con géneros dinámicos
        self.genero_var = tk.StringVar(value="Todos")
        self.combo_genero = ttk.Combobox(right_frame, textvariable=self.genero_var,
                                         values=opciones_genero, state="readonly")
        self.combo_genero.pack(fill="x", padx=15, pady=5)


        # --- Filtro por calificación ---
        tk.Label(right_frame, text="Calificación mínima:", bg="#FFFB00", fg="black",
                 font=("Helvetica", 12)).pack(anchor="w", padx=15, pady=(10, 0))
        self.rating_var = tk.DoubleVar(value=0.0)
        tk.Scale(right_frame, from_=0, to=5, resolution=0.5,
                 orient="horizontal", variable=self.rating_var,
                 bg="#FFFB00", highlightthickness=0).pack(fill="x", padx=15, pady=5)

        # --- Botón de aplicar filtro ---
        tk.Button(right_frame, text="Aplicar filtro", font=("Helvetica", 12, "bold"),
                  bg="black", fg="white", activebackground="#333",
                  command=self.aplicar_filtros).pack(pady=15)

        # Cargar películas
        self.cargar_peliculas()

    # === FUNCIONES ===

    def aplicar_filtros(self):
        genero_sel = self.genero_var.get()
        calificacion_min = self.rating_var.get()

        # Limpia las tarjetas actuales
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        peliculas = films.get("mainPage")

        for peli in peliculas:
            # Obtener y normalizar valores
            promedio = peli.get("promedio_calificacion", 0.0)
            if promedio is None:
                promedio = 0.0  # Si viene None, se trata como 0.0

            genero = peli.get("genero", "")

            # Convertir el género a texto (si es lista)
            if isinstance(genero, list):
                genero_texto = " ".join(genero).lower()
            else:
                genero_texto = str(genero).lower()

            # Aplicar filtro
            if (genero_sel == "Todos" or genero_sel.lower() in genero_texto) and float(promedio) >= calificacion_min:
                self._crear_card(peli)


    def recargar_pagina(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.actualizar_generos()
        self.cargar_peliculas()
        
        messagebox.showinfo("PopRate", "Página recargada correctamente ✅")

    def cargar_peliculas(self):
        peliculas = films.get("mainPage")
        for peli in peliculas:
            self._crear_card(peli)

    def _crear_card(self, data):
        card = tk.Frame(self.scrollable_frame, bg="#1e1e1e", bd=0, highlightthickness=0)
        card.pack(pady=15, padx=30, fill="x")

        tk.Label(card, text=data['nombre'], font=("Helvetica", 18, "bold"),
                 fg="#FFD700", bg="#1e1e1e").pack(anchor="w", padx=15, pady=(10, 2))

        frame_rating = tk.Frame(card, bg="#1e1e1e")
        frame_rating.pack(anchor="w", padx=15)

        total_reseñas = data.get("total_reseñas", 0)
        if total_reseñas > 0:
            promedio = data.get("promedio_calificacion", 0.0)
            try:
                promedio = round(float(promedio), 1)
            except (TypeError, ValueError):
                promedio = 0.0

            tk.Label(frame_rating, text="⭐", font=("Helvetica", 14),
                     fg="#FFD700", bg="#1e1e1e").pack(side="left")
            tk.Label(frame_rating, text=f"{promedio:.1f}",
                     font=("Helvetica", 12, "bold"),
                     fg="#FFD700", bg="#1e1e1e").pack(side="left", padx=(5, 0))
        else:
            tk.Label(frame_rating, text="Rate It!",
                     font=("Helvetica", 15, "italic"),
                     fg="#AAAAAA", bg="#1e1e1e").pack(side="left")

        tk.Label(card, text=f"{'Película' if data['tipo'] == 1 else 'Serie'} | {data['año']}",
                 font=("Helvetica", 12), fg="#CCCCCC", bg="#1e1e1e").pack(anchor="w", padx=15)

        tk.Label(card, text=f"Género: {data['genero']}", font=("Helvetica", 12),
                 fg="#CCCCCC", bg="#1e1e1e").pack(anchor="w", padx=15)

        tk.Label(card, text=f"Sinopsis: {data['sinopsis']}", font=("Helvetica", 12),
                 fg="#EEEEEE", bg="#1e1e1e", wraplength=1200, justify="left").pack(anchor="w", padx=15, pady=(5, 10))

        tk.Button(card, text="Ver más", font=("Helvetica", 12, "bold"),
                  bg="#FFD700", fg="#1e1e1e", activebackground="#FFC107",
                  command=lambda d=data: self.ver_mas(d)).pack(anchor="e", padx=15, pady=(0, 10))

    def ver_mas(self, data):
        movie_id = str(data['_id'])
        ventana_detalle = tk.Toplevel(self)
        ventana_detalle.geometry("1280x720")
        ventana_detalle.title(data['nombre'])
        ventana_detalle.configure(bg="#121212")
        detalle = FrameDetailMovie(ventana_detalle, movie_id=movie_id)
        detalle.pack(fill="both", expand=True)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ver_cuenta(self):
        ventana = tk.Toplevel(self)
        ventana.geometry("1280x720")
        ventana.title("Mi perfil")
        ventana.configure(bg="#121212")
        FrameProfile(ventana).pack(fill="both", expand=True)

    def agregar_pelicula(self):
        ventana = tk.Toplevel(self)
        ventana.geometry("700x700")
        ventana.title("Agregar Película")
        ventana.configure(bg="#1E1E1E")
        FrameAddMovie(ventana).pack(fill="both", expand=True)

    def ver_actores(self):
        ventana = tk.Toplevel(self)
        ventana.geometry("1280x720")
        ventana.title("Actores")
        ventana.configure(bg="#121212")
        FrameActors(ventana).pack(fill="both", expand=True)

    def ver_directores(self):
        ventana = tk.Toplevel(self)
        ventana.geometry("1280x720")
        ventana.title("Directores")
        ventana.configure(bg="#121212")
        from pages.directors import FrameDirectors
        FrameDirectors(ventana).pack(fill="both", expand=True)

    def actualizar_generos(self):
        """Regenera dinámicamente el listado de géneros según las películas disponibles."""
        peliculas = films.get("mainPage")
        generos_unicos = set()

        for peli in peliculas:
            genero = peli.get("genero", [])
            if isinstance(genero, list):
                generos_unicos.update(genero)
            elif isinstance(genero, str):
                generos_unicos.add(genero)

        generos_ordenados = sorted(list(generos_unicos))
        opciones_genero = ["Todos"] + generos_ordenados

        # Actualiza los valores del combobox
        self.combo_genero["values"] = opciones_genero

        # Reinicia la selección actual
        self.genero_var.set("Todos")