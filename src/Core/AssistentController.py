from src.Types.AssistentTypeSolicitude import AssistentTypeSolicitude as mode
from src.Core.Handlers.BaseHandler import BaseHandler


class AssistentController:
    """
    Owns the main loop and routes each mode to its registered handler.
    Never needs to change when new modes are added.
    """

    def __init__(self, ui):
        self.ui = ui
        self._handlers: dict[mode, BaseHandler] = {}

    def register(self, mode_type: mode, handler: BaseHandler) -> None:
        self._handlers[mode_type] = handler

    async def run(self) -> None:
        print(f"{self.ui.name} is starting up...\n")


        while True:
            self.ui.show_menu()
            selected_mode = self.ui.get_option()

            if selected_mode == mode.EXIT:
                print("Bye Bye!")
                break

            handler = self._handlers.get(selected_mode)
            if handler:
                await handler.run()
            else:
                print(f"⚠️  No handler registered for {selected_mode}.")