from AssistentTypeSolicitude import AssistentTypeSolicitude as option


class User:
    def __init__(self, mode: option):
        self.type = mode
        self.question: str = ""

        if self.type == option.QUESTIONS:
            self.question = input("Ask: ")

        elif self.type == option.PLAY_MUSIC:
            self.question = input("What song do you want to play? ")

        elif self.type == option.EXIT:
            print("Bye Bye!")

    def __str__(self):
        return self.question



