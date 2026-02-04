import customtkinter
import sklearn as kit #TODO: decidir sí usar Support Vector Machines o Decision Trees.
import os
import tempfile

#añade la pantalla de carga "splash.png"
if "NUITKA_ONEFILE_PARENT" in os.environ:
    splash_filename = os.path.join(
        tempfile.gettempdir(),
        "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"])
    )
    if os.path.exists(splash_filename):
        os.unlink(splash_filename)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        """datos iniciales de la aplicación"""
        self.title("Inserte título de la aplicación")
        self.geometry("400x150")
        self.grid_columnconfigure((0,1), weight=1)
        #TODO: separar los atributos en clases conforme vaya avanzando la aplicación.
        self.button = customtkinter.CTkButton(self, text="botoncito", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
    def button_callback(self):
        print("¡Luces, cámara, acción!")

app = App()
app.mainloop()

"""
Args:
Returns:
Raises:
Example:
https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
"""