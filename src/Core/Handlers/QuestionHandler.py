from src.Core.Handlers.BaseHandler import BaseHandler
from src.Services.AIModelsApi import LLMClient
from src.Services.VoiceOutput import VoiceOutput


class QuestionHandler(BaseHandler):
    """
    Handles the Q&A conversation loop.
    - Typing → streams response to terminal
    - Voice  → gets full response then speaks it
    """

    def __init__(self, ui):
        super().__init__(ui)
        self._llm = LLMClient()
        self._voice_out = VoiceOutput()

    async def run(self) -> None:
        for question in self.ui.input_loop("You: ", "Ask me anything!"):
            if self.ui.voice_mode:
                await self._respond_voice(question)
            else:
                await self._respond_text(question)
            print()

    async def _respond_text(self, question: str) -> None:
        """Stream response word by word to terminal."""
        await self._llm.chat_stream(question)

    async def _respond_voice(self, question: str) -> None:
        """Get full response, print it and speak it out loud."""
        reply = await self._llm.chat(question)
        print(f"Cortana: {reply}")
        await self._voice_out.speak(reply)