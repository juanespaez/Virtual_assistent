from NaturalLanguajeModel import *

class BertResponse():

    def __init__(self, qainput):
        self.qainput = qainput

    def bertanswer(self):
        bert = Bert(self.qainput)  # Inicializamos la clase Bert
        answer = bert.loadmodel()  # Ejecutamos el metodo
        realanswer = answer.get('answer')
        return realanswer

