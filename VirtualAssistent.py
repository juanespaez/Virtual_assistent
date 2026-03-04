import asyncio
from AssistentSelectionType import AssistentTypeSolicitude as mode
from User import User
from Database import Database


class VirtualAssistent:

    def __init__(self, name: str = "Cortana"):
        self.name = name

    def welcome(self) -> mode:
        print(f"""
            Hello! My name is {self.name}, I'm here to help you.
            What do you want to do?
              1. Ask a question
              2. Play a song
              3. Exit
        """)
        option = int(input("Choose an option: "))
        return self.decision_filter(option)

    def decision_filter(self, option: int) -> mode:
        if option == 1:
            return mode.QUESTIONS
        elif option == 2:
            return mode.PLAY_MUSIC
        else:
            return mode.EXIT

    async def run(self):
        """Main loop — keeps the assistant running until the user exits."""
        print(f"{self.name} is starting up...")

        while True:
            selected_mode = self.welcome()
            user = User(selected_mode)

            if selected_mode == mode.EXIT:
                break

            db = Database(selected_mode.value, str(user))
            await db.run()
            print()  # spacing between interactions


# Entry point
if __name__ == "__main__":
    assistant = VirtualAssistent(name="Cortana")
    asyncio.run(assistant.run())