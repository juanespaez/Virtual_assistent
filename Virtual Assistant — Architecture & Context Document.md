# 🤖 Virtual Assistant — Architecture & Context Document

## Quick Context (for starting a new conversation)

> Copy and paste this block at the start of a new chat to give full context instantly:

---

**PROJECT CONTEXT:**
I am building a personal home assistant in Python (like Jarvis/Cortana) using an OOP architecture.
Here is the current state of the project:

**What it can do:**
- Chat with an LLM via OpenRouter free API (text and voice mode)
- Play music on YouTube via pywhatkit
- Voice input via SpeechRecognition (press V to activate, say "bye bye" to deactivate)
- Voice output via Edge TTS (Microsoft Aria neural voice — human sounding)

**Architecture principles we follow strictly:**
- Single Responsibility — every class does ONE thing
- No DRY violations — repeated patterns are abstracted
- OOP only — no mixing classes with pure functions
- Open/Closed — adding a new feature never modifies existing classes

**How to add a new feature (the pattern we use):**
1. Add new mode to `src/Types/AssistentTypeSolicitude.py` enum
2. Add it to the menu in `src/UI/VirtualAssistent.py`
3. Create `src/Core/Handlers/YourHandler.py` inheriting from `BaseHandler`
4. Register it in `src/Core/Handlers/registry.py`
— `main.py`, `AssistentController`, `BaseHandler`, `LLMClient` never change.

**Tech stack:** Python 3.12, openai (OpenRouter), edge-tts, pygame, SpeechRecognition, pyaudio, pywhatkit, python-dotenv

---

## Project Structure

```
Virtual_assistent/
│   .env                          ← API keys (never commit)
│   main.py                       ← Entry point, never changes
│
└───src/
    ├───Core/
    │   │   AssistentController.py
    │   │
    │   └───Handlers/
    │           BaseHandler.py
    │           QuestionHandler.py
    │           MusicHandler.py
    │           registry.py
    │
    ├───Services/
    │       AIModelsApi.py
    │       VoiceInput.py
    │       VoiceOutput.py
    │
    ├───Types/
    │       AssistentTypeSolicitude.py
    │
    └───UI/
            VirtualAssistent.py
```

---

## Class Reference

### `main.py`
**Responsibility:** Boot the app. Never changes.
- Loads `.env`
- Creates `VirtualAssistent` and `AssistentController`
- Calls `register_all_handlers()`
- Runs the async event loop

---

### `src/UI/VirtualAssistent.py` — `VirtualAssistent`
**Responsibility:** Terminal UI only — menus, prompts, input handling.
- `show_menu()` — prints the option menu
- `get_option()` — reads and validates the user's menu choice
- `input_loop(label, hint)` — reusable generator that handles the while loop for all handlers. Supports both typing and voice mode. Yields user input until "back" is said/typed
- `voice_mode` — read-only property, tells handlers if voice is currently active
- Typing `v` activates voice mode, saying "bye bye" deactivates it

---

### `src/Core/AssistentController.py` — `AssistentController`
**Responsibility:** Main loop and routing. Never changes when new features are added.
- `register(mode, handler)` — registers a `BaseHandler` for a given mode
- `run()` — main while loop, shows menu, gets option, calls the right handler

---

### `src/Core/Handlers/BaseHandler.py` — `BaseHandler` *(abstract)*
**Responsibility:** Contract that all handlers must follow.
- Every handler must inherit from this and implement `async run()`
- Stores `self.ui` reference to `VirtualAssistent`

---

### `src/Core/Handlers/QuestionHandler.py` — `QuestionHandler`
**Responsibility:** Handles the Q&A conversation loop.
- `run()` — iterates `ui.input_loop()`, routes to text or voice response
- `_respond_text()` — streams LLM reply word by word to terminal
- `_respond_voice()` — gets full LLM reply, prints it and speaks it via `VoiceOutput`
- Owns its own `LLMClient` instance (preserves conversation history per session)

---

### `src/Core/Handlers/MusicHandler.py` — `MusicHandler`
**Responsibility:** Handles music playback loop.
- `run()` — iterates `ui.input_loop()`, plays each song on YouTube via pywhatkit

---

### `src/Core/Handlers/registry.py` — `register_all_handlers()`
**Responsibility:** The ONLY place that connects modes to handler instances.
- Import your new handler here and call `controller.register()` to add it
- Nothing else needs to change when adding a new feature

---

### `src/Services/AIModelsApi.py` — `LLMClient`
**Responsibility:** Reusable OpenRouter API wrapper with conversation memory.
- Tries 5 free models in order, best conversational quality first:
  1. `arcee-ai/trinity-large-preview:free`
  2. `meta-llama/llama-4-maverick:free`
  3. `deepseek/deepseek-chat-v3-0324:free`
  4. `deepseek/deepseek-r1:free`
  5. `openrouter/free` (guaranteed fallback)
- Auto-falls back to next model on 400, 404, 429 errors
- `chat(input)` — returns full response string, keeps history
- `chat_stream(input)` — streams response word by word to terminal
- `reset()` — clears conversation history
- `history` — read-only property of conversation so far
- System prompt tells the model to respond conversationally (no markdown/bullet points)

---

### `src/Services/VoiceInput.py` — `VoiceInput`
**Responsibility:** Microphone input via Google Speech Recognition (free, needs internet).
- `listen()` — listens for up to 5 seconds for speech, 10 seconds max phrase length
- Returns transcribed text or `None` if nothing was understood
- Used by `VirtualAssistent.input_loop()` when voice mode is active

---

### `src/Services/VoiceOutput.py` — `VoiceOutput`
**Responsibility:** Text-to-speech via Microsoft Edge TTS neural voices (free, needs internet).
- `async speak(text)` — generates and plays audio using Edge TTS
- Default voice: `en-US-AriaNeural` (natural female, Cortana-like)
- Other good voices: `en-US-JennyNeural`, `en-US-GuyNeural`, `en-GB-SoniaNeural`
- Uses `pygame` to play the generated mp3
- Used by `QuestionHandler._respond_voice()` when voice mode is active

---

### `src/Types/AssistentTypeSolicitude.py` — `AssistentTypeSolicitude`
**Responsibility:** Enum of all available assistant modes.
```python
class AssistentTypeSolicitude(enum.Enum):
    QUESTIONS  = 1
    PLAY_MUSIC = 2
    EXIT       = 3
```

---

## How the Layers Communicate

```
main.py
  ├── VirtualAssistent        (UI)
  ├── AssistentController     (routing)
  └── register_all_handlers() (wiring)
          │
          ├── QuestionHandler
          │     ├── LLMClient      (text replies)
          │     └── VoiceOutput    (speaks replies)
          │
          └── MusicHandler
                └── pywhatkit      (YouTube playback)

VirtualAssistent
  └── VoiceInput               (microphone listening)
```

---

## Voice Mode Flow

```
User types 'v'
  → voice mode ON
  → VoiceInput.listen() called after each response
  → QuestionHandler._respond_voice() used instead of _respond_text()
  → LLMClient.chat() gets full reply
  → VoiceOutput.speak() reads it out loud
  → listens again automatically

User says 'bye bye'
  → voice mode OFF
  → back to typing

User says/types 'back'
  → returns to main menu
```