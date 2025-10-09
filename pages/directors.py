import tkinter as tk
from tkinter import ttk
from database.conection import conect

class FrameDirectors(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#121212")
        tk.Label(self, text="Directores", font=("Helvetica", 20, "bold"), fg="#FFD700", bg="#121212").pack(pady=30)

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
        tk.Label(subtitulo_frame, text="Directores", font=("Helvetica", 16, "bold"), fg="#FFD700", bg="#121212").pack(side="left")
        tk.Button(subtitulo_frame, text="Agregar", font=("Helvetica", 12, "bold"),
                  bg="#3E8E41", fg="white", activebackground="#4CAF50",
                  command=self.agregar_director).pack(side="left", padx=10)

        self.mostrar_directores()

    def mostrar_directores(self):
        # Elimina los directores actuales antes de refrescar
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.scrollable_frame.winfo_children()[0]:
                widget.destroy()
        for director in self.obtener_directores(completo=True):
            card = tk.Frame(self.scrollable_frame, bg="#1e1e1e", bd=0, highlightthickness=0, width=900)
            card.pack(pady=5, fill="x", padx=0, ipadx=30)
            # Nombre
            tk.Label(card, text=director.get("nombre_completo", ""), font=("Helvetica", 14, "bold"),
                     fg="#FFD700", bg="#1e1e1e", anchor="w", width=60).pack(anchor="w", padx=30, pady=(10,2))
            # Género
            tk.Label(card, text=f"Género: {director.get('genero', '')}", font=("Helvetica", 12),
                     fg="#CCCCCC", bg="#1e1e1e", anchor="w").pack(anchor="w", padx=30, pady=(0,2))
            # Biografía
            tk.Label(card, text=f"Biografía: {director.get('biografia', '')}", font=("Helvetica", 12),
                     fg="#CCCCCC", bg="#1e1e1e", anchor="w", wraplength=800, justify="left").pack(anchor="w", padx=30, pady=(0,2))
            # Fecha de nacimiento
            tk.Label(card, text=f"Fecha de nacimiento: {director.get('fecha_nacimiento', '')}", font=("Helvetica", 12),
                     fg="#CCCCCC", bg="#1e1e1e", anchor="w").pack(anchor="w", padx=30, pady=(0,10))

            # Botones Modificar y Eliminar
            btn_frame = tk.Frame(card, bg="#1e1e1e")
            btn_frame.pack(anchor="e", padx=30, pady=(0,10))
            tk.Button(btn_frame, text="Modificar", font=("Helvetica", 11, "bold"),
                      bg="#FFD700", fg="#1e1e1e", activebackground="#FFC107",
                      command=lambda d=director: self.modificar_director(d)).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Eliminar", font=("Helvetica", 11, "bold"),
                      bg="#E84141", fg="white", activebackground="#FF6666",
                      command=lambda d=director: self.eliminar_director(d)).pack(side="left", padx=5)

    def obtener_directores(self, completo=False):
        collection = conect("actors_directors")
        if completo:
            return list(collection.find({"tipo": 1}, {"_id": 1, "nombre_completo": 1, "biografia": 1, "fecha_nacimiento": 1, "genero": 1}))
        else:
            return list(collection.find({"tipo": 1}, {"_id": 1, "nombre_completo": 1}))

    def agregar_director(self):
        form = tk.Toplevel(self)
        form.title("Agregar Director")
        form.geometry("420x400")
        form.configure(bg="#121212")

        main_frame = tk.Frame(form, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main_frame, text="Agregar Director", font=("Helvetica", 16, "bold"), fg="#FFD700", bg="#121212").pack(pady=(0,15))

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
                    "tipo": 1
                })
                form.destroy()
                self.mostrar_directores()
            else:
                tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def eliminar_director(self, director):
        from tkinter import messagebox
        if messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar a {director.get('nombre_completo', '')}?"):
            collection = conect("actors_directors")
            collection.delete_one({"_id": director["_id"]})
            self.mostrar_directores()

    def modificar_director(self, director):
        form = tk.Toplevel(self)
        form.title("Modificar Director")
        form.geometry("420x400")
        form.configure(bg="#121212")

        main_frame = tk.Frame(form, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main_frame, text="Modificar Director", font=("Helvetica", 16, "bold"), fg="#FFD700", bg="#121212").pack(pady=(0,15))

        campo_bio = tk.Frame(main_frame, bg="#121212")
        campo_bio.pack(fill="x", pady=7)
        tk.Label(campo_bio, text="Biografía:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        entry_bio = tk.Entry(campo_bio, font=("Helvetica", 12), width=24, bg="#232323", fg="#FFD700", insertbackground="#FFD700", relief="flat")
        entry_bio.pack(side="left", padx=8)
        entry_bio.insert(0, director.get("biografia", ""))

        campo_fecha = tk.Frame(main_frame, bg="#121212")
        campo_fecha.pack(fill="x", pady=7)
        tk.Label(campo_fecha, text="Fecha de nacimiento:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        entry_fecha = tk.Entry(campo_fecha, font=("Helvetica", 12), width=24, bg="#232323", fg="#FFD700", insertbackground="#FFD700", relief="flat")
        entry_fecha.pack(side="left", padx=8)
        entry_fecha.insert(0, director.get("fecha_nacimiento", ""))

        campo_genero = tk.Frame(main_frame, bg="#121212")
        campo_genero.pack(fill="x", pady=7)
        tk.Label(campo_genero, text="Género:", font=("Helvetica", 12), fg="#FFD700", bg="#121212", width=16, anchor="w").pack(side="left")
        combo_genero = ttk.Combobox(campo_genero, font=("Helvetica", 12), width=22, state="readonly")
        combo_genero["values"] = ("M", "F")
        combo_genero.pack(side="left", padx=8)
        combo_genero.set(director.get("genero", "M"))

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
                    {"_id": director["_id"]},
                    {"$set": {
                        "biografia": biografia,
                        "fecha_nacimiento": fecha,
                        "genero": genero
                    }}
                )
                form.destroy()
                self.mostrar_directores()
            else:
                tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")