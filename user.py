

class User:
    def __init__(self, type_s):
        self.type = type_s
        self.question = ""

        if self.type == 1:
            self.question = input("ask: ").__str__()

        elif self.type == 2:
            self.question = input("What do you want to know? ")

        elif self.type == 3:
            self.question = input("What song you want to play? ").__str__()

    def __str__(self):
        return self.question




