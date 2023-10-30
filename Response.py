from NaturalLanguajeModel import *
from base_interface import *

class BertResponse(BertResponseBase):

    def __init__(self, qainput):
        self.qainput = qainput

    def bertanswer(self):
        bert = Bert(self.qainput)  # Inicializamos la clase Bert
        answer = bert.loadmodel()  # Ejecutamos el metodo
        realanswer = answer.get('answer')
        return realanswer

