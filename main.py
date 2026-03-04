import asyncio
from VirtualAssistent import VirtualAssistent
from AssistentController import AssistentController

if __name__ == "__main__":
    try:
        ui = VirtualAssistent(name="Cortana")
        controller = AssistentController(ui=ui)
        asyncio.run(controller.run())
    except KeyboardInterrupt:
        print("invalid input")