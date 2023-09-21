

class User:
    def __init__(self, type_s):
        self.type = type_s
        self.question = "" # empyty string as default string

        if self.type == 1:
            self.question = input("ask: ").__str__() # we use the __str__ so the program later ca read it as a str type

        elif self.type == 2:
            self.question = input("What do you want to know? ") # during the code it was unnecessary to use __str__ here

        elif self.type == 3:
            self.question = input("What song you want to play? ").__str__()

        elif self.type == 4:
            qainput = dict()
            question = input("What is your question? ")
            qainput['question'] = question
            context = input('Enter the context to answer the question: ')
            qainput['context'] = context
            self.question = qainput

    def __str__(self): # funtion that lets the question be return with no issues 
        return self.question




