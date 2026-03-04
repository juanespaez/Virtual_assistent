import pyttsx3


class VoiceOutput:
    """
    Handles text-to-speech output.
    Uses pyttsx3 — works fully offline, no API needed.
    """

    def __init__(self, rate: int = 175, volume: float = 1.0):
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", rate)       # speed: 150-200 is natural
        self._engine.setProperty("volume", volume)   # 0.0 to 1.0
        self._set_voice()

    def speak(self, text: str) -> None:
        """Speak the given text out loud."""
        self._engine.say(text)
        self._engine.runAndWait()

    def _set_voice(self) -> None:
        """Try to use a female English voice if available."""
        voices = self._engine.getProperty("voices")
        for voice in voices:
            if "zira" in voice.name.lower() or "female" in voice.name.lower():
                self._engine.setProperty("voice", voice.id)
                return
        # fallback to first available voice
        if voices:
            self._engine.setProperty("voice", voices[0].id)