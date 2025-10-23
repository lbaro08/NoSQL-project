import tkinter as tk
from tkinter import ttk
from database.conection import conect

class FrameActors(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#121212")
        tk.Label(self, text="Actores", font=("Helvetica", 20, "bold"), fg="#FFD700", bg="#121212").pack(pady=30)

        listado_container = tk.Frame(self, bg="#121212")
        listado_container.pack(fill="both", expand=True, padx=30, pady=10)

        canvas = tk.Canvas(listado_container, bg="#121212", highlightthickness=0)
        scrollbar = tk.Scrollbar(listado_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#121212")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Subtítulo y botón agregar
        subtitulo_frame = tk.Frame(self.scrollable_frame, bg="#121212")
        subtitulo_frame.pack(fill="x", pady=(0,5))
        tk.Label(subtitulo_frame, text="Actores", font=("Helvetica", 16, "bold"), fg="#FFD700", bg="#121212").pack(side="left")
        tk.Button(subtitulo_frame, text="Agregar", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=self.agregar_actor).pack(side="left", padx=10)

        self.mostrar_actores()

    def mostrar_actores(self):
        # Elimina los actores actuales antes de refrescar
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.scrollable_frame.winfo_children()[0]:
                widget.destroy()
        for actor in self.obtener_actores(completo=True):
            card = tk.Frame(self.scrollable_frame, bg="#1e1e1e", bd=0, highlightthickness=0, width=900)
            card.pack(pady=5, fill="x", padx=0, ipadx=30)
            # Nombre
            tk.Label(card, text=actor.get("nombre_completo", ""), font=("Helvetica", 14, "bold"),
                     fg="#FFD700", bg="#1e1e1e", anchor="w", width=60).pack(anchor="w", padx=30, pady=(10,2))
            # Género
            tk.Label(card, text=f"Género: {actor.get('genero', '')}", font=("Helvetica", 12),
                     fg="#CCCCCC", bg="#1e1e1e", anchor="w").pack(anchor="w", padx=30, pady=(0,2))
            # Biografía
            tk.Label(card, text=f"Biografía: {actor.get('biografia', '')}", font=("Helvetica", 12),
                     fg="#CCCCCC", bg="#1e1e1e", anchor="w", wraplength=800, justify="left").pack(anchor="w", padx=30, pady=(0,2))
            # Fecha de nacimiento
            tk.Label(card, text=f"Fecha de nacimiento: {actor.get('fecha_nacimiento', '')}", font=("Helvetica", 12),
                     fg="#CCCCCC", bg="#1e1e1e", anchor="w").pack(anchor="w", padx=30, pady=(0,10))

            # Botones Modificar y Eliminar
            btn_frame = tk.Frame(card, bg="#1e1e1e")
            btn_frame.pack(anchor="e", padx=30, pady=(0,10))
            tk.Button(btn_frame, text="Modificar", font=("Helvetica", 11, "bold"),
                      bg="#FFD700", fg="#1e1e1e", activebackground="#FFC107",
                      command=lambda a=actor: self.modificar_actor(a)).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Eliminar", font=("Helvetica", 11, "bold"),
                      bg="#E84141", fg="white", activebackground="#FF6666",
                      command=lambda a=actor: self.eliminar_actor(a)).pack(side="left", padx=5)

    def obtener_actores(self, completo=False):
        collection = conect("actors_directors")
        if completo:
            return list(collection.find({"tipo": 0}, {"_id": 1, "nombre_completo": 1, "biografia": 1, "fecha_nacimiento": 1, "genero": 1}))
        else:
            return list(collection.find({"tipo": 0}, {"_id": 1, "nombre_completo": 1}))

    def agregar_actor(self):
        # Ventana de formulario
        form = tk.Toplevel(self)
        form.title("Agregar Actor")
        form.geometry("420x440")
        form.configure(bg="#121212")

        main_frame = tk.Frame(form, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main_frame, text="Agregar Actor", font=("Helvetica", 16, "bold"), fg="#FFD700", bg="#121212").pack(pady=(0,15))

        campo_nombre = tk.Frame(main_frame, bg="#121212")
        campo_nombre.pack(fill="x", pady=7)
        tk.Label(campo_nombre, text="Nombre completo:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        entry_nombre = tk.Entry(campo_nombre, font=("Helvetica", 12), width=24, bg="#232323", fg="#FFD700", insertbackground="#FFD700", relief="flat")
        entry_nombre.pack(side="left", padx=8)

        campo_bio = tk.Frame(main_frame, bg="#121212")
        campo_bio.pack(fill="x", pady=7)
        tk.Label(campo_bio, text="Biografía:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        entry_bio = tk.Entry(campo_bio, font=("Helvetica", 12), width=24, bg="#232323", fg="#FFD700", insertbackground="#FFD700", relief="flat")
        entry_bio.pack(side="left", padx=8)

        campo_fecha = tk.Frame(main_frame, bg="#121212")
        campo_fecha.pack(fill="x", pady=7)
        tk.Label(campo_fecha, text="Fecha de nacimiento:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        entry_fecha = tk.Entry(campo_fecha, font=("Helvetica", 12), width=24, bg="#232323", fg="#FFD700", insertbackground="#FFD700", relief="flat")
        entry_fecha.pack(side="left", padx=8)

        campo_genero = tk.Frame(main_frame, bg="#121212")
        campo_genero.pack(fill="x", pady=7)
        tk.Label(campo_genero, text="Género:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        from tkinter import ttk
        combo_genero = ttk.Combobox(campo_genero, font=("Helvetica", 12), width=22, state="readonly")
        combo_genero["values"] = ("M", "F")
        combo_genero.pack(side="left", padx=8)
        combo_genero.current(0)

        tk.Button(main_frame, text="Guardar", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=lambda: guardar()).pack(pady=25, ipadx=10, ipady=3)

        def guardar():
            nombre = entry_nombre.get().strip()
            biografia = entry_bio.get().strip()
            fecha = entry_fecha.get().strip()
            genero = combo_genero.get().strip()
            if nombre and biografia and fecha and genero:
                collection = conect("actors_directors")
                collection.insert_one({
                    "nombre_completo": nombre,
                    "biografia": biografia,
                    "fecha_nacimiento": fecha,
                    "genero": genero,
                    "tipo": 0
                })
                form.destroy()
                self.mostrar_actores()
            else:
                tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def mostrar_info_actor(self, actor):
        info = f"Nombre: {actor.get('nombre_completo', '')}\n"
        info += f"Película: {actor.get('pelicula', '')}\n"
        info += f"Biografía: {actor.get('biografia', '')}\n"
        info += f"Fecha de nacimiento: {actor.get('fecha_nacimiento', '')}"
        tk.messagebox.showinfo("Información del actor", info)

    def eliminar_actor(self, actor):
        from tkinter import messagebox
        if messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar a {actor.get('nombre_completo', '')}?"):
            collection = conect("actors_directors")
            collection.delete_one({"_id": actor["_id"]})
            self.mostrar_actores()

    def modificar_actor(self, actor):
        form = tk.Toplevel(self)
        form.title("Modificar Actor")
        form.geometry("420x400")
        form.configure(bg="#121212")

        main_frame = tk.Frame(form, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main_frame, text="Modificar Actor", font=("Helvetica", 16, "bold"), fg="#FFD700", bg="#121212").pack(pady=(0,15))

        campo_bio = tk.Frame(main_frame, bg="#121212")
        campo_bio.pack(fill="x", pady=7)
        tk.Label(campo_bio, text="Biografía:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        entry_bio = tk.Entry(campo_bio, font=("Helvetica", 12), width=24, bg="#232323", fg="#FFD700", insertbackground="#FFD700", relief="flat")
        entry_bio.pack(side="left", padx=8)
        entry_bio.insert(0, actor.get("biografia", ""))

        campo_fecha = tk.Frame(main_frame, bg="#121212")
        campo_fecha.pack(fill="x", pady=7)
        tk.Label(campo_fecha, text="Fecha de nacimiento:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        entry_fecha = tk.Entry(campo_fecha, font=("Helvetica", 12), width=24, bg="#232323", fg="#FFD700", insertbackground="#FFD700", relief="flat")
        entry_fecha.pack(side="left", padx=8)
        entry_fecha.insert(0, actor.get("fecha_nacimiento", ""))

        campo_genero = tk.Frame(main_frame, bg="#121212")
        campo_genero.pack(fill="x", pady=7)
        tk.Label(campo_genero, text="Género:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        combo_genero = ttk.Combobox(campo_genero, font=("Helvetica", 12), width=22, state="readonly")
        combo_genero["values"] = ("M", "F")
        combo_genero.pack(side="left", padx=8)
        combo_genero.set(actor.get("genero", "M"))

        tk.Button(main_frame, text="Guardar cambios", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=lambda: guardar()).pack(pady=25, ipadx=10, ipady=3)

        def guardar():
            biografia = entry_bio.get().strip()
            fecha = entry_fecha.get().strip()
            genero = combo_genero.get().strip()
            if biografia and fecha and genero:
                collection = conect("actors_directors")
                collection.update_one(
                    {"_id": actor["_id"]},
                    {"$set": {
                        "biografia": biografia,
                        "fecha_nacimiento": fecha,
                        "genero": genero
                    }}
                )
                form.destroy()
                self.mostrar_actores()
            else:
                tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")