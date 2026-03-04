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
        self._voice_mode = False
        self._menu_options: dict[int, tuple[str, mode]] = {
            1: ("Ask a question", mode.QUESTIONS),
            2: ("Play a song",    mode.PLAY_MUSIC),
            0: ("Exit",           mode.EXIT),
        }

    @property
    def voice_mode(self) -> bool:
        return self._voice_mode

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
        Reusable input generator — supports typing and voice.
        - Type 'v' once to switch to voice mode (stays on)
        - Say or type 'back' to return to the menu
        - Say or type 'bye bye' to exit voice mode back to typing
        """
        print(f"\n{hint}")
        print("Type 'back' to return to menu | Type 'v' to enable voice mode\n")

        while True:
            if self._voice_mode:
                value = self._voice_input.listen()  # listen() prints its own messages
                if value is None:
                    continue
            else:
                value = input(label).strip()
                if not value:
                    continue
                if value.lower() == "v":
                    self._voice_mode = True
                    print("🎤 Voice mode ON — say 'bye bye' to switch back to typing.\n")
                    continue

            # Check control words before yielding to handler
            if value.lower() == "back":
                self._voice_mode = False
                return

            if value.lower() in ("bye bye", "bye-bye"):
                self._voice_mode = False
                print("⌨️  Voice mode OFF — back to typing.\n")
                continue

            yield value