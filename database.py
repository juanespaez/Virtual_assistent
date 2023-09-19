import requests
from bs4 import BeautifulSoup as bs
import pywhatkit
import wikipedia


class Database:
    def __init__(self, question, search):
        self.question = question  # tiene  solo un atributo con el cual jugaremos con las demas funciones
        self.search = search

        if self.question == 1:  # esto se cambiara por "si el modelo no cumple cierto requisito
            self.ultimate_search()  # llame la clase procesamiento de lenguage natural"

        elif self.question == 2:
            self.specific_search()

        elif self.question == 3:
            self.play_music()

    def ultimate_search(self):
        url = f"https://www.google.com/search?q={self.search}"  # creando el url para conectarlo

        req = requests.get(url)
        soup = bs(req.text, "html.parser")  # creamos el soup variable en el cual se guarda el htlm de la busqueda

        my_search = soup.find("div",
                              class_="BNeawe").text  # encontramos la clase en el html que contiene la respuesta y la
        # extraemos para imprimirla
        print(my_search)

    def play_music(self):
        print(self.search)
        search = str(self.search)
        if "play" in search:
            pywhatkit.playonyt(search)

    def specific_search(self):
        print(self.search)
        search = str(self.search)
        if ("who is" in search) or ("what is" in search) or ("who was" in search):
            info = wikipedia.summary(search, 2)
            print(info)

    def database_search(self):
        pass # aun no tenemso nada que poner pero aqui ira el codigo que tendra el modelo de busqueda en la base de
        # datos y el modole que verificara si la respuesta es buena o no
