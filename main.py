from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

import asyncio
from src.UI.VirtualAssistent import VirtualAssistent
from src.Core.AssistentController import AssistentController
from src.Core.Handlers.Registry import register_all_handlers


if __name__ == "__main__":
    try:
        ui = VirtualAssistent(name="Cortana")
        controller = AssistentController(ui=ui)
        register_all_handlers(controller, ui)
        asyncio.run(controller.run(



        ))
    except KeyboardInterrupt:
        print("\nGoodbye!")