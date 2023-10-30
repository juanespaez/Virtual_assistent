class BertResponseBase:
    def bertanswer(self):
        raise NotImplementedError("Subclases deben implementar el método bertanswer")

    #NotImplementedError. Las subclases que deseen proporcionar respuestas utilizando
    # BERT deben heredar de esta clase base y proporcionar su propia implementación para el método bertanswer.