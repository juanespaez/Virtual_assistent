import asyncio
from src.Core.VirtualAssistent import VirtualAssistent
from src.Core.AssistentController import AssistentController

if __name__ == "__main__":
    try:
        ui = VirtualAssistent(name="Cortana")
        controller = AssistentController(ui=ui)
        asyncio.run(controller.run())
    except KeyboardInterrupt:
        print("invalid input")