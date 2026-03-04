from src.Types.AssistentTypeSolicitude import AssistentTypeSolicitude as mode
from src.Core.Handlers.BaseHandler import BaseHandler
from src.Services.IntentDetector import IntentDetector


class AssistentController:
    """
    Controls the main loop and routes each input to its handler via intent detection.
    No menu — the user just talks and the assistant decides what to do.
    """

    def __init__(self, ui):
        self.ui = ui
        self._handlers: dict[mode, BaseHandler] = {}
        self._intent_detector = IntentDetector()

    def register(self, mode_type: mode, handler: BaseHandler) -> None:
        self._handlers[mode_type] = handler

    async def run(self) -> None:
        print(f"\n{self.ui.name} is ready! Just talk to me.")
        print("Type 'v' to use voice. Type or say 'exit' to quit.\n")

        while True:
            user_input = await self.ui.get_input()

            if not user_input:
                continue

            # Detect intent
            detected_mode = await self._intent_detector.detect(user_input)

            if detected_mode == mode.EXIT:
                print("Bye Bye!")
                break

            handler = self._handlers.get(detected_mode)
            if handler:
                await handler.handle(user_input)
            else:
                print(f"⚠️  No handler registered for {detected_mode}.")