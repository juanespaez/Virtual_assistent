from src.Core.Handlers.BaseHandler import BaseHandler
from src.Services.AIModelsApi import LLMClient
from src.Services.VoiceOutput import VoiceOutput


class QuestionHandler(BaseHandler):
    """
    Handles Q&A — receives a question and responds.
    - Typing → streams response word by word
    - Voice  → gets full response and speaks it
    """

    def __init__(self, ui, llm: LLMClient):
        super().__init__(ui)
        self._llm = llm
        self._voice_out = VoiceOutput()

    async def handle(self, user_input: str) -> None:
        if self.ui.voice_mode:
            await self._respond_voice(user_input)
        else:
            await self._respond_text(user_input)
        print()

    async def _respond_text(self, question: str) -> None:
        await self._llm.chat_stream(question)

    async def _respond_voice(self, question: str) -> None:
        reply = await self._llm.chat(question)
        print(f"Cortana: {reply}")
        await self._voice_out.speak(reply)