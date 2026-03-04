import os
from openai import AsyncOpenAI
from dotenv import load_dotenv


class LLMClient:
    """
    Reusable LLM client using OpenRouter's free tier.

    Usage:
        llm = LLMClient()
        llm = LLMClient(system_prompt="You are a cooking expert.")
        reply = await llm.chat("Hello!")
        await llm.chat_stream("Hello!")
        llm.reset()

    Free models ranked best for conversational/voice use:
        1. arcee-ai/trinity-large-preview:free   — best for voice/chat
        2. meta-llama/llama-4-maverick:free      — great general assistant
        3. deepseek/deepseek-chat-v3-0324:free   — strong conversation
        4. deepseek/deepseek-r1:free             — great reasoning
        5. openrouter/free                       — auto picks (guaranteed fallback)
    """

    MODELS = [
        "arcee-ai/trinity-large-preview:free",
        "meta-llama/llama-4-maverick:free",
        "deepseek/deepseek-chat-v3-0324:free",
        "deepseek/deepseek-r1:free",
        "openrouter/free",  # always last — guaranteed fallback
    ]

    def __init__(self, system_prompt: str = (
        "You are Cortana, a fast and helpful personal home assistant. "
        "Keep your responses concise and conversational. "
        "You are also speaking out loud so avoid bullet points, "
        "markdown formatting, or long lists. Speak naturally."
    )):
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

    async def chat(self, user_input: str) -> str:
        """Send a message and get a full response string. Remembers history."""
        self._history.append({"role": "user", "content": user_input})
        for model in self.MODELS:
            try:
                response = await self._client.chat.completions.create(
                    model=model,
                    messages=self._build_messages(),
                )
                reply = response.choices[0].message.content or ""
                self._history.append({"role": "assistant", "content": reply})
                return reply
            except Exception as e:
                if any(code in str(e) for code in ("400", "404", "429")):
                    continue  # try next model
                self._history.pop()
                raise RuntimeError(f"LLM request failed: {e}") from e

        self._history.pop()
        raise RuntimeError("All models failed.")

    async def chat_stream(self, user_input: str) -> str:
        """Stream response to stdout word by word. Also returns full reply."""
        self._history.append({"role": "user", "content": user_input})
        for model in self.MODELS:
            try:
                response = await self._client.chat.completions.create(
                    model=model,
                    messages=self._build_messages(),
                    stream=True,
                )
                full_reply = ""
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)
                        full_reply += content
                print()
                self._history.append({"role": "assistant", "content": full_reply})
                return full_reply
            except Exception as e:
                if any(code in str(e) for code in ("400", "404", "429")):
                    continue  # try next model
                self._history.pop()
                raise RuntimeError(f"LLM stream failed: {e}") from e

        self._history.pop()
        raise RuntimeError("All models failed.")

    def reset(self) -> None:
        """Clear conversation history, keeps system prompt."""
        self._history = []

    @property
    def history(self) -> list[dict]:
        return list(self._history)

    def _build_messages(self) -> list[dict]:
        return [{"role": "system", "content": self._system_prompt}, *self._history]