from click.exceptions import Exit
from src.Types.AssistentTypeSolicitude import AssistentTypeSolicitude as mode
from src.Core.Handlers.QuestionHandler import QuestionHandler
from src.Core.Handlers.MusicHandler import MusicHandler
# from src.Core.handlers.WeatherHandler import WeatherHandler


def register_all_handlers(controller, ui) -> None:
    """
    The ONLY place where modes are connected to their handlers.
    To add a new feature:
      1. Create src/Core/handlers/YourHandler.py
      2. Add your mode to AssistentTypeSolicitude
      3. Add your option to VirtualAssistent menu
      4. Import and register it here — nothing else changes.
    """
    controller.register(mode.QUESTIONS,  QuestionHandler(ui))
    controller.register(mode.PLAY_MUSIC, MusicHandler(ui))
    controller.register(mode.EXIT, Exit(ui))
