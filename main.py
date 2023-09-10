# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from Interface import *

window = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
window.title("Home page")
window.geometry("600x400")
label = ctk.CTkLabel(master=window, text="Sing in ")  # tittle
label.pack(pady=12, padx=10)

button = ctk.CTkButton(master=window, text="login", command=login)
button.pack(pady=12, padx=10)
# Creamos el espacio entre el primer boton y el segundo boton


window.mainloop()
