from AssistentTypeSolicitude import AssistentTypeSolicitude as mode
from VirtualAssistent import VirtualAssistent
from AssistentModes import AssistentModes


class AssistentController:
    """
    Owns the main loop and all conversation flows.
    Connects the UI (VirtualAssistent) with the actions (Database).
    """

    def __init__(self, ui: VirtualAssistent):
        self.ui = ui

    async def run(self):
        """Main loop — runs until the user exits."""
        print(f"{self.ui.name} is starting up...\n")

        while True:
            self.ui.show_menu()
            selected_mode = self.ui.get_option()

            if selected_mode == mode.EXIT:
                print("Bye Bye!")
                break

            elif selected_mode == mode.QUESTIONS:
                await self._question_loop()

            elif selected_mode == mode.PLAY_MUSIC:
                await self._music_loop()
            else:
                print("Invalid option!")

    async def _question_loop(self):
        """Conversation loop — keeps chatting until user types 'back'."""
        self.ui.print_back_hint("Ask me anything!")
        db = AssistentModes(mode.QUESTIONS.value, "")

        while True:
            question = self.ui.prompt_question()
            if not question:
                continue
            if question.lower() == "back":
                break

            db.search = question
            await db.run()
            print()

    async def _music_loop(self):
        """Music loop — keeps playing songs until user types 'back'."""
        self.ui.print_back_hint("What song do you want to play?")

        while True:
            song = self.ui.prompt_song()
            if not song:
                continue
            if song.lower() == "back":
                break

            db = AssistentModes(mode.PLAY_MUSIC.value, song)
            await db.run()
            print()