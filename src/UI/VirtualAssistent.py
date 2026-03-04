from src.Types.AssistentTypeSolicitude import AssistentTypeSolicitude as mode
from src.Services.VoiceInput import VoiceInput


class VirtualAssistent:
    """
    Responsible only for UI — showing menus and reading user input.
    Supports both typed and voice input.
    """

    def __init__(self, name: str = "Cortana"):
        self.name = name
        self._voice_input = VoiceInput()
        self._menu_options: dict[int, tuple[str, mode]] = {
            1: ("Ask a question", mode.QUESTIONS),
            2: ("Play a song",    mode.PLAY_MUSIC),
            3: ("Exit",           mode.EXIT),
        }

    def show_menu(self) -> None:
        print(f"\nHello! My name is {self.name}, I'm here to help you.")
        print("What do you want to do?")
        for key, (label, _) in self._menu_options.items():
            print(f"  {key}. {label}")
        print()

    def get_option(self) -> mode:
        while True:
            try:
                option = int(input("Choose an option: "))
                if option in self._menu_options:
                    return self._menu_options[option][1]
                print(f"❌ Please enter a number between 1 and {len(self._menu_options)}.\n")
            except ValueError:
                print("❌ Invalid input, please enter a number.\n")

    def input_loop(self, label: str, hint: str):
        """
        Reusable input generator — supports both typing and voice (press V).
        Yields user input until 'back' is typed or said.
        """
        print(f"\n{hint} Type 'back' to return to the menu. Press V to use voice.\n")
        while True:
            value = input(label).strip()

            if not value:
                continue

            # Voice input trigger
            if value.lower() == "v":
                spoken = self._voice_input.listen()
                if spoken is None:
                    continue
                value = spoken

            if value.lower() == "back":
                return

            yield value