import requests
from bs4 import BeautifulSoup as bs


class Database:
    def __init__(self, question):
        self.question = question  # tiene  solo un atributo con el cual jugaremos con las demas funciones
        if self.question == "lebron james age":  # esto se cambiara por "si el modelo no cumple cierto requisito
            # llame la clase procesamiento de lenguage natural"
            self.ultimate_search()

    def ultimate_search(self):
        url = f"https://www.google.com/search?q={self.question}"  # creando el url para conectarlo

        req = requests.get(url)
        soup = bs(req.text, "html.parser")  # creamos el soup variable en el cual se guarda el htlm de la busqueda

        my_search = soup.find("div",
                              class_="BNeawe").text  # encontramos la clase en el html que contiene la respuesta y la
        # extraemos para imprimirla
        print(my_search)

    def Database_Search(self):
        pass  # aun no tenemso nada que poner pero aqui ira el codigo que tendra el modelo de busqueda en la base de
        # datos y el modole que verificara si la respuesta es buena o no
