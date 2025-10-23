import tkinter as tk
from tkinter import ttk, messagebox
from database import films
from functions.session import Session
from datetime import datetime
from bson import ObjectId
from database import reviews

class FrameDetailMovie(tk.Frame):
    def __init__(self, parent, movie_id):
        super().__init__(parent, width=1280, height=720, bg="#121212")
        self.pack_propagate(False)

        print("Sera quie si?",movie_id)
        self.movie_id = movie_id
        self.movie_data = films.get('filmDetailsOpc',movie_id)
        print(self.movie_data)

        # Contenedor principal
        self.content_frame = tk.Frame(self, bg="#121212")
        self.content_frame.pack(fill="both", expand=True)

        self.reviews_data = [
            {"usuario": "Juan", "calificacion": 5, "comentario": "Obra maestra absoluta."},
            {"usuario": "Ana", "calificacion": 4, "comentario": "Muy buena, aunque larga."}
        ]

        self.build_ui()

    def build_ui(self):
        movie_data = self.movie_data
        self.reviews_data = movie_data['reseñas']
        if movie_data is None:
            movie_data = {
                "nombre": "El Padrino",
                "tipo": "Película",
                "año": 1972,
                "genero": ["Crimen", "Drama"],
                "sinopsis": "La historia de la familia Corleone y su ascenso en el mundo del crimen…",
                "directores": ["Francis Ford Coppola"],
                "actores": ["Marlon Brando", "Al Pacino", "James Caan"]
            }

        # ----- Info superior -----
        info_frame = tk.Frame(self.content_frame, bg="#1E1E1E")
        info_frame.pack(fill="x", padx=50, pady=20)

        tk.Label(info_frame, text=movie_data["nombre"], font=("Arial", 32, "bold"),
                 fg="#FFD700", bg="#1E1E1E").pack(anchor="w")
        tipo = "Película" if movie_data.get("tipo") == 1 else "Serie"
        tk.Label(info_frame,
                 text=f"{tipo} | {movie_data['año']} | {', '.join(movie_data['genero'])}",
                 font=("Arial", 16), fg="white", bg="#1E1E1E").pack(anchor="w", pady=(5,10))
        tk.Label(info_frame, text=movie_data["sinopsis"], font=("Arial", 14),
                 fg="white", bg="#1E1E1E", wraplength=1180, justify="left").pack(anchor="w")

        tk.Label(info_frame, text="Directores: " + ", ".join(movie_data.get("directores", [])),
                 font=("Arial", 14), fg="white", bg="#1E1E1E").pack(anchor="w", pady=(5,0))
        tk.Label(
            info_frame,
            text="Actores: " + ", ".join([f'{a["nombre"]} ({a["personaje"]})' for a in movie_data.get("elenco", [])]),
            font=("Arial", 14),
            fg="white",
            bg="#1E1E1E"
        ).pack(anchor="w", pady=(0,10))


        # ----- Reseñas -----
        review_frame = tk.Frame(self.content_frame, bg="#121212")
        review_frame.pack(fill="both", expand=True, padx=50, pady=(0,10))

        canvas = tk.Canvas(review_frame, bg="#121212", highlightthickness=0)
        scrollbar = ttk.Scrollbar(review_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#121212")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.display_reviews()

        # ----- Input nueva reseña -----
        input_frame = tk.Frame(self.content_frame, bg="#1E1E1E")
        input_frame.pack(fill="x", padx=50, pady=10)

        tk.Label(input_frame, text="Comentario:", fg="white", bg="#1E1E1E", font=("Arial", 12)).grid(row=1, column=0, sticky="nw", pady=2)
        self.comentario_entry = tk.Text(input_frame, width=80, height=4, font=("Arial", 12))
        self.comentario_entry.grid(row=1, column=1, pady=2, padx=5)

        tk.Label(input_frame, text="Calificación (0-5):", fg="white", bg="#1E1E1E", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=2)
        self.calificacion_entry = tk.Spinbox(input_frame, from_=0, to=5, width=5, font=("Arial", 12))
        self.calificacion_entry.grid(row=2, column=1, sticky="w", pady=2, padx=5)

        tk.Button(input_frame, text="Enviar Reseña", font=("Arial", 12, "bold"),
                  bg="#FFD700", fg="#121212", command=self.add_review).grid(row=3, column=1, sticky="e", pady=10)

    def display_reviews(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for r in self.reviews_data:
            card = tk.Frame(self.scrollable_frame, bg="#1E1E1E", bd=2, relief="ridge")
            card.pack(fill="x", pady=10)
            tk.Label(card, text=f'{r["nombre_usuario"]} - {r["calificacion"]} ⭐',
                     font=("Arial", 18, "bold"), fg="#FFD700", bg="#1E1E1E").pack(anchor="w", padx=10, pady=(5,0))
            tk.Label(card, text=r["texto_reseña"], font=("Arial", 16),
                     fg="white", bg="#1E1E1E", wraplength=1100, justify="left").pack(anchor="w", padx=10, pady=(0,5))

    def add_review(self):
        comentario = self.comentario_entry.get("1.0", "end").strip()
        try:
            calificacion = int(self.calificacion_entry.get())
        except ValueError:
            messagebox.showerror("Error", "La calificación debe ser un número de 0 a 5")
            return

        if not comentario or calificacion < 0 or calificacion > 5:
            messagebox.showerror("Error", "Completa todos los campos correctamente")
            return

        user_data = Session.user
        new_review = {
            "id_usuario": ObjectId(user_data.get("_id")),
            "id_pelicula_serie": ObjectId(self.movie_id),
            "nombre_usuario": user_data.get("nombre_usuario"),  # para mostrar en display_reviews
            "calificacion": calificacion,
            "texto_reseña": comentario,
            "fecha_publicacion": datetime.utcnow(),  # fecha actual en UTC
            "votos_utilidad": 0
        }

        result = reviews.putReview(user_data.get("_id"),self.movie_id,new_review)

        if result == 1:
            messagebox.showerror("Error", "Ya tienes una resena")
            self.master.destroy()  # cierra toda la ventana
        elif result ==2:
            messagebox.showerror("Error", "Error inesperado al insertar la resena")
            self.master.destroy()  # cierra toda la ventana
        else :
            self.display_reviews()
            self.comentario_entry.delete("1.0", "end")
            self.calificacion_entry.delete(0, "end")
            self.calificacion_entry.insert(0, "0")
            messagebox.showinfo("Exito", "Se inserto la resena")
            self.master.destroy()  # cierra toda la ventana
        return
            


        


