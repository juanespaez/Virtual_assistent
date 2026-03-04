import pywhatkit
from api_implementation import LLMClient


class Database:
    def __init__(self, question: int, search: str):
        self.question = question  # the option number chosen (1, 2, 3...)
        self.search = search      # the actual text the user typed

    async def run(self):
        """Call this after creating the Database instance to execute the action."""
        if self.question == 1:
            await self.model_use()

        elif self.question == 2:
            self.play_music()

    async def model_use(self):
        model_client = LLMClient()
        await model_client.chat_stream(self.search)

    def play_music(self):
        print(f"Searching for: {self.search}")
        search = str(self.search)
        if "play" in search.lower():
            pywhatkit.playonyt(search)
        else:
            # Add "play" prefix if the user didn't include it
            pywhatkit.playonyt(f"play {search}")

    def __str__(self):
        return self.search