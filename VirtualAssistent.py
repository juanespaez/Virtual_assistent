class VirtualAssistent:

    def __init__(self, name='Cortana'):
        self.name = name

    def welcome(self):
        print(f"""Hello, my name is {self.name}, i'm here for help you.
        What do you want to do?
        1. General knowledge question
        2. Specific search
        3. Play a song
        4. Question with context
        5. Exit
        6. NEW MODEL IN PROCESS WANNA CHAT WITH A NEW FRIEND
        > """)

        option = int(input('Choose one option: '))
        return option
