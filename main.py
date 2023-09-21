# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from Interface import *
from VirtualAssistent import *
from User import *
from NaturalLanguajeModel import *
from Response import *

while True:
    Cortana = VirtualAssistent()
    option = Cortana.welcome()
    if option == 1:
        pass
    elif option == 2:
        pass
    elif option == 3:
        pass

    elif option == 4:
        doubt = User(option)
        bert = BertResponse(doubt.question)
        answer = bert.bertanswer()
        print(answer)
        print('-'*20)
        change = input(print('Do you wanna use the same context?: '))
        while change.lower() == 'yes':
            new_doubt = input("What is your new question?: ")
            doubt.question['question'] = new_doubt
            bert = BertResponse(doubt.question)
            answer = bert.bertanswer()
            print(answer)
            print('-'*20)
            change = input(print('Do you wanna use the same context?: '))

    elif option == 5:
        print('Bye Bye')
        break













pantalla_principal()

type_search = int(input("""What is your desire?
    1 - general question knowledge theme
    2 - specific question search
    3 - play a song
    > """))
search = User(type_search)

Database(type_search, search)
