from AssistentTypeSolicitude import AssistentTypeSolicitude as mode


class VirtualAssistent:
    """
    Only responsible for UI — showing menus and reading user input.
    No logic, no loops, no decisions.
    """

    def __init__(self, name: str = "Cortana"):
        self.name = name

    def show_menu(self):
        print(f"""
            Hello! My name is {self.name}, I'm here to help you.
            What do you want to do?
              1. Ask a question
              2. Play a song
              3. Exit
        """)

    def get_option(self) -> mode:
        while True:
            try:
                option = int(input("Choose an option: "))
                return self._parse_option(option)
            except ValueError:
                print(" Invalid input, please enter 1, 2 or 3.\n")

    def _parse_option(self, option: int) -> mode:
        if option == 1:
            return mode.QUESTIONS
        elif option == 2:
            return mode.PLAY_MUSIC
        else:
            return mode.EXIT

    def prompt_question(self) -> str:
        return input("You: ").strip()

    def prompt_song(self) -> str:
        return input("Song: ").strip()

    def print_back_hint(self, context: str):
        print(f"\n{context} Type 'back' to return to the menu.\n")