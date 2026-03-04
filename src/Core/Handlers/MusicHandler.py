import pywhatkit
from src.Core.Handlers.BaseHandler import BaseHandler
from src.Services.AIModelsApi import LLMClient


class MusicHandler(BaseHandler):
    """
    Handles music playback.
    Uses LLM to extract the best YouTube search query from natural language.
    e.g. "play Future's latest album" → "Future High Off Life album"
    """

    _SYSTEM_PROMPT = """
You are a music search assistant. 
Given a user request, respond with ONLY the best YouTube search query to find that music.
No explanation, no quotes, just the search query.

Examples:
"play Future" → Future best songs
"play Future's latest album" → Future I Never Liked You album
"play something relaxing" → relaxing chill music playlist
"I want to hear some hip hop" → best hip hop playlist 2024
"play Blinding Lights" → The Weeknd Blinding Lights
"""

    def __init__(self, ui):
        super().__init__(ui)
        self._llm = LLMClient(system_prompt=self._SYSTEM_PROMPT)

    async def handle(self, user_input: str) -> None:
        print("🎵 Finding the best match...")
        query = await self._llm.chat(user_input)
        query = query.strip()
        print(f"🎵 Playing: {query}")
        pywhatkit.playonyt(query)
        print()