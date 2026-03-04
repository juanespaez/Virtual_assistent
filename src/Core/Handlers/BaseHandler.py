from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """
    Abstract base class for all mode handlers.
    Every handler must inherit from this and implement run().
    """

    def __init__(self, ui):
        self.ui = ui

    @abstractmethod
    async def run(self) -> None:
        """Execute the handler loop for this mode."""
        pass