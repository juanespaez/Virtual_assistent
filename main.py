# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from Interface import *
from VirtualAssistent import *
from User import *
from NaturalLanguajeModel import *
from Response import *
from database import *

while True:
    Cortana = VirtualAssistent()
    option = Cortana.welcome()
    if option == 1:
        search = User(option)
        Database(option, search)

    elif option == 2:
        search = User(option)
        answer = Database(option, search)
        answer2 = answer.specific_search()
        print(answer2)

    elif option == 3:
        search = User(option)
        Database(option, search)

    elif option == 4:
        doubt = User(option)  # Inicializamos usuario 
        bert = BertResponse(doubt.question) #Inicializamos el modelo 
        answer = bert.bertanswer()  # Ejecutamos el metodo bertanswer
        print(answer)  #Mostramos en pantalla la respuesta 
        print('-'*20)
        change = input(print('Do you wanna use the same context?: '))
        while change.lower() == 'yes':
            new_doubt = input("What is your new question?: ")
            doubt.question['question'] = new_doubt  #  Se cambia la pregunta
            bert = BertResponse(doubt.question)  
            answer = bert.bertanswer()
            print(answer)
            print('-'*20)
            change = input(print('Do you wanna use the same context?: '))

    elif option == 5:
        print('Bye Bye')
        break
        
    elif option == 6:
        friend()
