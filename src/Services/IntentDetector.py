from src.Services.AIModelsApi import LLMClient
from src.Types.AssistentTypeSolicitude import AssistentTypeSolicitude as mode


class IntentDetector:
    """
    Uses a dedicated LLMClient to classify user input into an intent.
    Completely separate from the conversation LLMClient so it never
    pollutes the conversation history.
    """

    # System prompt focused purely on classification — no chat
    _SYSTEM_PROMPT = """
You are an intent classifier for a personal home assistant.
Given a user message, respond with ONLY one of these exact labels — nothing else:

QUESTIONS   — the user wants to ask something, have a conversation, or get information
PLAY_MUSIC  — the user wants to play music, a song, an artist, an album or a playlist
EXIT        — the user wants to quit, exit, goodbye, stop the assistant

Examples:
"who is einstein" → QUESTIONS
"what time is it" → QUESTIONS
"tell me a joke" → QUESTIONS
"play Future" → PLAY_MUSIC
"play something relaxing" → PLAY_MUSIC
"play Future's latest album" → PLAY_MUSIC
"I want to hear some hip hop" → PLAY_MUSIC
"put on some music" → PLAY_MUSIC
"exit" → EXIT
"goodbye" → EXIT
"bye" → EXIT

Respond with ONLY the label. No explanation, no punctuation, nothing else.
"""

    def __init__(self):
        self._llm = LLMClient(system_prompt=self._SYSTEM_PROMPT)

    async def detect(self, user_input: str) -> mode:
        """Classify user input and return the matching mode."""
        result = await self._llm.chat(user_input)
        label = result.strip().upper()

        if "PLAY_MUSIC" in label:
            return mode.PLAY_MUSIC
        elif "EXIT" in label:
            return mode.EXIT
        else:
            return mode.QUESTIONS  # default fallback