import speech_recognition as sr


class VoiceInput:
    """
    Handles voice input via microphone.
    Uses Google Speech Recognition (free, requires internet).
    """

    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._recognizer.pause_threshold = 1.0   # seconds of silence before stopping
        self._recognizer.energy_threshold = 300  # mic sensitivity

    def listen(self) -> str | None:
        """
        Listen from the microphone and return the transcribed text.
        Returns None if speech was not understood or an error occurred.
        """
        with sr.Microphone() as source:
            print("🎤 Listening... (speak now)")
            self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self._recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                print("⚠️  No speech detected.")
                return None
            except sr.UnknownValueError:
                print("⚠️  Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                return None