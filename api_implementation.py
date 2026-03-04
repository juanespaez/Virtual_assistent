import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """
    Reusable LLM client using OpenRouter's free tier.

    Usage:
        llm = LLMClient()                         # default: Home Assistant
        llm = LLMClient(system_prompt="You are a cooking expert.")  # custom persona

        response = await llm.chat("Hello!")       # single message, no memory
        response = await llm.ask("Hello!")        # alias for chat()

        await llm.chat_stream("Hello!")           # stream to stdout

        llm.reset()                               # clear conversation history
    """

    MODEL = "openrouter/free"

    def __init__(self, system_prompt: str = "You are a fast, helpful Home Assistant."):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or "YOUR_OPENROUTER_KEY" in api_key:
            raise EnvironmentError(
                "❌ OPENROUTER_API_KEY is missing or invalid.\n"
                "Add it to your .env file: OPENROUTER_API_KEY=sk-or-v1-..."
            )

        self._client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self._system_prompt = system_prompt
        self._history: list[dict] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def chat(self, user_input: str) -> str:
        """
        Send a message and get a full response string back.
        Remembers conversation history automatically.

        Example:
            reply = await llm.chat("What's the weather like?")
            print(reply)
        """
        self._history.append({
            "role": "user",
            "content": user_input
        })
        messages = self._build_messages()

        try:
            response = await self._client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
            )
            reply = response.choices[0].message.content or ""
            self._history.append({"role": "assistant", "content": reply})
            return reply

        except Exception as e:
            self._history.pop()  # remove user message on failure
            raise RuntimeError(f"LLM request failed: {e}") from e

    # Friendly alias
    ask = chat

    async def chat_stream(self, user_input: str) -> str:
        """
        Send a message and stream the response to stdout in real time.
        Also returns the full reply as a string when done.

        Example:
            await llm.chat_stream("Tell me a story.")
        """
        self._history.append({"role": "user", "content": user_input})
        messages = self._build_messages()

        try:
            response = await self._client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                stream=True,
            )

            full_reply = ""
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_reply += content

            print()  # newline after stream ends
            self._history.append({"role": "assistant", "content": full_reply})
            return full_reply

        except Exception as e:
            self._history.pop()
            raise RuntimeError(f"LLM stream failed: {e}") from e

    def reset(self):
        """Clear conversation history (keeps system prompt)."""
        self._history = []

    @property
    def history(self) -> list[dict]:
        """Read-only view of the conversation history."""
        return list(self._history)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_messages(self) -> list[dict]:
        """Prepend system prompt to current history."""
        return [
            {"role": "system", "content": self._system_prompt},
            *self._history,
        ]


# ------------------------------------------------------------------
# Standalone runner — python llm_client.py
# ------------------------------------------------------------------

async def main():
    llm = LLMClient()
    print("🏠 Home Assistant ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        print("Assistant: ", end="")
        try:
            await llm.chat_stream(user_input)
        except RuntimeError as e:
            print(f"\n❌ {e}")
        print()


if __name__ == "__main__":
    asyncio.run(main())