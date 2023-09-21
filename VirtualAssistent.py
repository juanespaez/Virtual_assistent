from Response import *


class VirtualAssistent:

    def __init__(self, name, task):
        self.name = name
        self.task = task

    def welcome(self):
        print(f"""Hello, my name is {self.name}, i'm here for help you.
        What do you want to do?
        1. 
        2.
        3.
        4. Question with context """)

        option = int(input('Choose one option: '))
        return option
