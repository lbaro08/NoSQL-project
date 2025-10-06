import tkinter as tk
from tkinter import ttk, messagebox
from database import films
from database import actors_directors

# Listas de ejemplo; en producción podrían venir de la DB
LISTA_DIRECTORES = actors_directors.get('directors')
LISTA_ACTORES = actors_directors.get('actors')

class FrameAddMovie(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#1E1E1E")
        self.controller = controller

        # Scrollable frame
        self.canvas = tk.Canvas(self, bg="#1E1E1E", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1E1E1E")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        tk.Label(self.scrollable_frame, text="Agregar Nueva Película/Serie",
                 bg="#1E1E1E", fg="#FFD700", font=("Helvetica", 18, "bold")).pack(pady=20)

        # Campos básicos
        self.campos = {}
        self._crear_campos_basicos()

        # Géneros
        self.generos = []
        self._crear_campos_lista("Géneros", self.generos)

        # Directores con Combobox
        self.directores = []
        self._crear_combobox_lista("Directores", self.directores, LISTA_DIRECTORES)

        # Elenco con Actor (Combobox) + Personaje (Entry)
        self.elenco = []
        self._crear_elenco("Elenco (Actor - Personaje)", self.elenco, LISTA_ACTORES)

        # Botón Guardar
        tk.Button(self.scrollable_frame, text="Guardar", bg="#FFD700", fg="#1E1E1E", font=("Helvetica",12,"bold"),
                  command=self.guardar_pelicula).pack(pady=20)

    # -------------------------
    # Campos básicos: Título, Tipo, Año, Sinopsis
    # -------------------------
    def _crear_campos_basicos(self):
        # Título
        tk.Label(self.scrollable_frame, text="Título", bg="#1E1E1E", fg="white", font=("Helvetica",12)).pack(anchor="w", padx=20, pady=(10,0))
        self.campos["titulo"] = tk.StringVar()
        tk.Entry(self.scrollable_frame, textvariable=self.campos["titulo"], width=60,
                 bg="#2E2E2E", fg="white", insertbackground="white", font=("Helvetica",12)).pack(padx=20, pady=5)

        # Tipo
        tk.Label(self.scrollable_frame, text="Tipo", bg="#1E1E1E", fg="white", font=("Helvetica",12)).pack(anchor="w", padx=20, pady=(10,0))
        self.campos["tipo"] = tk.StringVar(value="1")
        tipo_combobox = ttk.Combobox(self.scrollable_frame, textvariable=self.campos["tipo"],
                                     values=["1 - Película","0 - Serie"], state="readonly", width=20, font=("Helvetica",12))
        tipo_combobox.pack(padx=20, pady=5)

        # Sinopsis
        tk.Label(self.scrollable_frame, text="Sinopsis", bg="#1E1E1E", fg="white", font=("Helvetica",12)).pack(anchor="w", padx=20, pady=(10,0))
        self.sinopsis_text = tk.Text(self.scrollable_frame, height=5, width=60, bg="#2E2E2E", fg="white",
                                     wrap="word", font=("Helvetica",12), insertbackground="white")
        self.sinopsis_text.pack(padx=20, pady=5)

        # Año
        tk.Label(self.scrollable_frame, text="Año de lanzamiento", bg="#1E1E1E", fg="white", font=("Helvetica",12)).pack(anchor="w", padx=20, pady=(10,0))
        self.campos["año"] = tk.StringVar()
        tk.Entry(self.scrollable_frame, textvariable=self.campos["año"], width=20, bg="#2E2E2E", fg="white", insertbackground="white",
                 font=("Helvetica",12)).pack(padx=20, pady=5)

    # -------------------------
    # Lista con Entry + Botón "Agregar"
    # -------------------------
    def _crear_campos_lista(self, label_text, lista):
        frame = tk.Frame(self.scrollable_frame, bg="#1E1E1E")
        frame.pack(fill="x", padx=20, pady=(10,0))

        tk.Label(frame, text=label_text, bg="#1E1E1E", fg="white", font=("Helvetica",12)).pack(anchor="w")

        entry_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=entry_var, width=40, bg="#2E2E2E", fg="white", insertbackground="white", font=("Helvetica",12))
        entry.pack(side="left", pady=5)

        listbox = tk.Listbox(frame, width=40, height=4, bg="#2E2E2E", fg="white", font=("Helvetica",12))
        listbox.pack(side="left", padx=(10,0))

        def agregar_item():
            val = entry_var.get().strip()
            if val and val not in lista:
                lista.append(val)
                listbox.insert("end", val)
                entry_var.set("")

        tk.Button(frame, text="Agregar", bg="#3E8E41", fg="white", font=("Helvetica",10,"bold"),
                  command=agregar_item).pack(side="left", padx=5)

    # -------------------------
    # Lista con Combobox + Botón "Agregar"
    # -------------------------
    def _crear_combobox_lista(self, label_text, lista, documentos):
        """
        documentos: lista de diccionarios de MongoDB, cada uno con 'nombre_completo' y 'tipo'
        """
        # Filtrar solo los documentos con tipo == 1
        opciones = [doc['nombre_completo'] for doc in documentos if doc.get('tipo') == 1]

        frame = tk.Frame(self.scrollable_frame, bg="#1E1E1E")
        frame.pack(fill="x", padx=20, pady=(10,0))

        tk.Label(frame, text=label_text, bg="#1E1E1E", fg="white", font=("Helvetica",12)).pack(anchor="w")

        combo_var = tk.StringVar()
        combobox = ttk.Combobox(frame, textvariable=combo_var, values=opciones, width=40, font=("Helvetica",12))
        combobox.pack(side="left", pady=5)

        listbox = tk.Listbox(frame, width=40, height=4, bg="#2E2E2E", fg="white", font=("Helvetica",12))
        listbox.pack(side="left", padx=(10,0))

        def agregar_item():
            val = combo_var.get().strip()
            if val and val not in lista:
                lista.append(val)
                listbox.insert("end", val)
                combo_var.set("")

        tk.Button(frame, text="Agregar", bg="#3E8E41", fg="white", font=("Helvetica",10,"bold"),
                command=agregar_item).pack(side="left", padx=5)

    # -------------------------
    # Elenco: Actor (Combobox) + Personaje (Entry)
    # -------------------------
    def _crear_elenco(self, label_text, lista, documentos):
        """
        documentos: lista de diccionarios de MongoDB, cada uno con '_id', 'nombre_completo' y 'tipo'
        """
        # Filtrar solo los documentos con tipo == 0 (actores)
        opciones = [doc['nombre_completo'] for doc in documentos if doc.get('tipo') == 0]
        # Crear un diccionario para buscar _id por nombre
        id_map = {doc['nombre_completo']: doc['_id'] for doc in documentos if doc.get('tipo') == 0}

        frame = tk.Frame(self.scrollable_frame, bg="#1E1E1E")
        frame.pack(fill="x", padx=20, pady=(10,0))

        tk.Label(frame, text=label_text, bg="#1E1E1E", fg="white", font=("Helvetica",12)).pack(anchor="w")

        actor_var = tk.StringVar()
        combobox = ttk.Combobox(frame, textvariable=actor_var, values=opciones, width=25, font=("Helvetica",12))
        combobox.pack(side="left", pady=5)

        personaje_var = tk.StringVar()
        tk.Entry(frame, textvariable=personaje_var, width=20, bg="#2E2E2E", fg="white", insertbackground="white", font=("Helvetica",12)).pack(side="left", padx=5)

        listbox = tk.Listbox(frame, width=40, height=4, bg="#2E2E2E", fg="white", font=("Helvetica",12))
        listbox.pack(side="left", padx=(10,0))

        def agregar_item():
            actor = actor_var.get().strip()
            personaje = personaje_var.get().strip()
            if actor and personaje:
                actor_id = id_map.get(actor)
                # Guardar objeto con _id y personaje
                val_obj = {"_id": actor_id, "personaje": personaje}
                print(val_obj)
                lista.append(val_obj)
                # Mostrar en Listbox solo el nombre y personaje
                listbox.insert("end", f"{actor} - {personaje}")
                actor_var.set("")
                personaje_var.set("")

        tk.Button(frame, text="Agregar", bg="#3E8E41", fg="white", font=("Helvetica",10,"bold"),
                command=agregar_item).pack(side="left", padx=5)

    # -------------------------
    # Guardar película/serie
    # -------------------------
    def guardar_pelicula(self):
        titulo = self.campos["titulo"].get().strip()
        tipo = self.campos["tipo"].get()[0]  # 1 o 0
        sinopsis = self.sinopsis_text.get("1.0","end").strip()
        año = self.campos["año"].get().strip()

        if not (titulo and sinopsis and año):
            messagebox.showerror("Error", "Título, sinopsis y año son obligatorios.")
            return
        if not self.generos:
            messagebox.showerror("Error", "Agrega al menos un género.")
            return
        if not self.directores:
            messagebox.showerror("Error", "Agrega al menos un director.")
            return
        if not self.elenco:
            messagebox.showerror("Error", "Agrega al menos un miembro del elenco.")
            return

        try:
            tipo = int(tipo)
            año = int(año)
        except ValueError:
            messagebox.showerror("Error", "Tipo y Año deben ser números.")
            return

        data = {
            "nombre": titulo,
            "tipo": tipo,
            "sinopsis": sinopsis,
            "año": año,
            "genero": self.generos.copy(),
            "directores": self.directores.copy(),
            "elenco": self.elenco.copy()
        }

        films.insert_one(data)
        messagebox.showinfo("Éxito", "Película/Serie agregada correctamente.")

        # Limpiar formulario
        self.campos["titulo"].set("")
        self.campos["tipo"].set("1")
        self.campos["año"].set("")
        self.sinopsis_text.delete("1.0","end")
        self.generos.clear()
        self.directores.clear()
        self.elenco.clear()
