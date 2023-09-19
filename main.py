# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from Interface import *
from user import *
from database import *

pantalla_principal()

type_search = int(input("""What is your desire?
    1 - general question knowledge theme
    2 - specific question search
    3 - play a song
    > """))
search = User(type_search)

Database(type_search, search)
