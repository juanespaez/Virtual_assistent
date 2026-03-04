import pywhatkit
from src.Core.Handlers.BaseHandler import BaseHandler


class MusicHandler(BaseHandler):
    """Handles the music playback loop."""

    async def run(self) -> None:
        for song in self.ui.input_loop("Song: ", "What song do you want to play?"):
            query = song if "play" in song.lower() else f"play {song}"
            pywhatkit.playonyt(query)
            print()