import tkinter as tk 
from pages.login import FrameLogin 
from pages.register import FrameRegister
from pages.startPage import FrameStartPage
from pages.detailMovie import FrameDetailMovie


class FramePrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#d1f0d1")

        label = tk.Label(self, text="Ventana Principal", font=("Arial", 20), bg="#d1f0d1")
        label.pack(pady=50)

        btn_cerrar = tk.Button(self, text="Cerrar sesión", command=lambda: controller.mostrar_frame("FrameLogin"))
        btn_cerrar.pack(pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("App con Login")
        self.geometry("1280x720")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Inicializamos los frames
        for F, nombre in zip((FrameLogin, FramePrincipal,FrameRegister,FrameStartPage), 
                             ("FrameLogin", "FramePrincipal","FrameRegister","FrameStartPage")):
            frame = F(container, self)
            self.frames[nombre] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostramos login al inicio
        self.mostrar_frame("FrameLogin")

    def mostrar_frame(self, nombre,movie_id=None):
        frame = self.frames[nombre]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()