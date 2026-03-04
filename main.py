import asyncio
from VirtualAssistent import VirtualAssistent

if __name__ == "__main__":
    assistant = VirtualAssistent(name="Cortana")
    asyncio.run(assistant.run())