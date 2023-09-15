import customtkinter as ctk


class slide_panel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master=parent)

        # general atributes
        self.start_pos = start_pos
        self.end_pos = end_pos - 0.03
        self.width = abs(start_pos - end_pos)

        # animation logic
        self.pos = start_pos
        self.in_start_pos = True

        # layout
        self.place(relx=start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backward()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backward(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backward)
        else:
            self.in_start_pos = True


def chat():
    window = ctk.CTk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    window.title("Cortana")
    window.geometry("600x400")

    animated_panel = slide_panel(window, 1.0, 0.7)
    ctk.CTkLabel(animated_panel, text="Hello, my name is Cortana").pack(expand=True, fill="both", padx=2, pady=10)
    ctk.CTkTextbox(animated_panel).pack(expand=True, fill="both")
    ctk.CTkButton(animated_panel, text="Send", corner_radius=0).pack(expand=True, fill="both", padx=2, pady=10)

    # botton
    button_x = 0.5
    button = ctk.CTkButton(window, text="Start", command=animated_panel.animate)
    button.place(relx=button_x, rely=0.5, anchor="center")

    # start
    window.mainloop()


def login():
    ctk.set_appearance_mode("dark")  # system, dark or light/ the color - background
    ctk.set_default_color_theme("dark-blue")  # darkblue, green, blue - login botton
    root = ctk.CTk()
    root.title("Login")
    root.geometry("500x300")
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame,
                         text="Welcome to our virtual asistent please enter the following steps: ")  # tittle
    label.pack(pady=12, padx=10)
    label = ctk.CTkLabel(master=frame, text="First add your username then your password: ")  # tittle
    label.pack(pady=12, padx=10)

    # pantalla2.geometry("500x300")   #create a window

    # Label(pantalla2, text = "").pack()  #some space in between

    # insert data
    user2 = ctk.CTkEntry(master=frame, placeholder_text="username")  # text box under the title
    user2.pack(pady=12, padx=10)

    entry2 = ctk.CTkEntry(master=frame, placeholder_text="password")  # text box under the title
    entry2.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="login", command=chat)  # botton using the login funtion
    button.pack(pady=12, padx=10)

    return root.mainloop()


def start():
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
