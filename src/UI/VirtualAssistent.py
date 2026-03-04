from src.Types.AssistentTypeSolicitude import AssistentTypeSolicitude as mode
from src.Services.VoiceInput import VoiceInput


class VirtualAssistent:
    """
    Responsible only for UI — getting input from the user.
    No menu needed anymore — intent detection handles routing.
    Supports both typed and voice input.
    """

    def __init__(self, name: str = "Cortana"):
        self.name = name
        self._voice_input = VoiceInput()
        self._voice_mode = False

    @property
    def voice_mode(self) -> bool:
        return self._voice_mode

    async def get_input(self) -> str | None:
        """
        Get input from user — typed or voice.
        Type 'v' to enable voice mode (stays on until 'bye bye').
        Returns None if nothing was captured.
        """
        if self._voice_mode:
            value = self._voice_input.listen()
            if value is None:
                return None
            if value.lower() in ("bye bye", "bye-bye"):
                self._voice_mode = False
                print("⌨️  Voice mode OFF — back to typing.\n")
                return None
            return value
        else:
            value = input("You: ").strip()
            if not value:
                return None
            if value.lower() == "v":
                self._voice_mode = True
                print("🎤 Voice mode ON — say 'bye bye' to switch back to typing.\n")
                return None
            return value