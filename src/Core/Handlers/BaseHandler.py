from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """
    Abstract base class for all mode handlers.
    Every handler must inherit from this and implement handle().
    handle() receives the user input directly — no inner loop needed
    since the main loop is now in AssistentController.
    """

    def __init__(self, ui):
        self.ui = ui

    @abstractmethod
    async def handle(self, user_input: str) -> None:
        """Execute the action for this mode with the given user input."""
        pass