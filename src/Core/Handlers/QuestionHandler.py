from src.Core.Handlers.BaseHandler import BaseHandler
from src.Services.AIModelsApi import LLMClient
from src.Services.VoiceOutput import VoiceOutput


class QuestionHandler(BaseHandler):
    """Handles the Q&A conversation loop with voice output."""

    def __init__(self, ui):
        super().__init__(ui)
        self._llm = LLMClient()
        self._voice_out = VoiceOutput()

    async def run(self) -> None:
        for question in self.ui.input_loop("You: ", "Ask me anything!"):
            reply = await self._llm.chat(question)
            print(f"Cortana: {reply}")
            self._voice_out.speak(reply)
            print()