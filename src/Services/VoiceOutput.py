import tempfile
import os
import edge_tts
import pygame


class VoiceOutput:
    """
    Handles text-to-speech using Microsoft Edge's neural voices.
    Sounds much more human than pyttsx3. Requires internet connection.

    Best English voices:
        en-US-AriaNeural      — natural female, great for assistants
        en-US-JennyNeural     — friendly female
        en-US-GuyNeural       — natural male
        en-US-EricNeural      — calm male
        en-GB-SoniaNeural     — British female
    """

    def __init__(self, voice: str = "en-US-AriaNeural", rate: str = "+0%", volume: str = "+0%"):
        self._voice = voice
        self._rate = rate
        self._volume = volume
        pygame.mixer.init()

    async def speak(self, text: str) -> None:
        """Speak the given text using Edge TTS neural voice."""
        communicate = edge_tts.Communicate(text, self._voice, rate=self._rate, volume=self._volume)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name

        try:
            await communicate.save(tmp_path)
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        finally:
            pygame.mixer.music.unload()
            os.remove(tmp_path)