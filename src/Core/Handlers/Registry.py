from src.Types.AssistentTypeSolicitude import AssistentTypeSolicitude as mode
from src.Core.Handlers.QuestionHandler import QuestionHandler
from src.Core.Handlers.MusicHandler import MusicHandler
from src.Services.AIModelsApi import LLMClient


def register_all_handlers(controller, ui) -> None:
    """
    The ONLY place where modes are connected to their handlers.
    LLMClient is created once and shared so conversation memory persists.
    """
    llm = LLMClient()  # shared conversation memory

    controller.register(mode.QUESTIONS,  QuestionHandler(ui, llm))
    controller.register(mode.PLAY_MUSIC, MusicHandler(ui))
