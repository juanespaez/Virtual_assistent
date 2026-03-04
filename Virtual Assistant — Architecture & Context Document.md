# 🤖 Virtual Assistant — Architecture & Context Document

## Quick Context (for starting a new conversation)

> Copy and paste this block at the start of a new chat to give full context instantly:

---

**PROJECT CONTEXT:**
I am building a personal home assistant in Python (like Jarvis/Cortana) using a strict OOP architecture.
Here is the current state of the project:

**What it can do:**
- Chat with an LLM via OpenRouter free API (text and voice mode)
- Play music on YouTube via pywhatkit — understands natural language ("play Future's latest album")
- Voice input via SpeechRecognition (type 'v' to activate, say "bye bye" to deactivate)
- Voice output via Edge TTS (Microsoft Aria neural voice — human sounding)
- Intent detection — no menu, just talk and the assistant decides what to do

**Architecture principles we follow strictly:**
- Single Responsibility — every class does ONE thing
- No DRY violations — repeated patterns are abstracted
- OOP only — no mixing classes with pure functions
- Open/Closed — adding a new feature never modifies existing classes
- Dependency Injection — shared instances passed in, not created internally

**How to add a new feature (the pattern we use):**
1. Add new mode to `src/Types/AssistentTypeSolicitude.py` enum
2. Add the new label to `src/Services/IntentDetector.py` system prompt
3. Create `src/Core/Handlers/YourHandler.py` inheriting `BaseHandler`, implement `handle(user_input)`
4. Register it in `src/Core/Handlers/registry.py`
— `main.py`, `AssistentController`, `BaseHandler`, `LLMClient`, `VirtualAssistent` never change.

**Tech stack:** Python 3.12, openai (OpenRouter), edge-tts, pygame, SpeechRecognition, pyaudio, pywhatkit, python-dotenv

**Install dependencies:**
```
pip install openai python-dotenv pywhatkit SpeechRecognition pyaudio edge-tts pygame
```

---

## Project Structure

```
Virtual_assistent/
│   .env                          ← API keys (never commit)
│   main.py                       ← Entry point, never changes
│
└───src/
    ├───Core/
    │   │   AssistentController.py   ← Main loop, routes by detected intent
    │   │
    │   └───Handlers/
    │           BaseHandler.py       ← Abstract contract: handle(user_input)
    │           QuestionHandler.py   ← Q&A, text stream or voice speak
    │           MusicHandler.py      ← LLM extracts query → pywhatkit plays it
    │           registry.py          ← Creates shared LLMClient, wires handlers
    │
    ├───Services/
    │       AIModelsApi.py           ← LLMClient, 5 model fallback chain, memory
    │       IntentDetector.py        ← Dedicated LLM that classifies intent only
    │       VoiceInput.py            ← Mic → text via Google Speech Recognition
    │       VoiceOutput.py           ← Text → speech via Edge TTS (Aria neural)
    │
    ├───Types/
    │       AssistentTypeSolicitude.py  ← Enum: QUESTIONS, PLAY_MUSIC, EXIT
    │
    └───UI/
            VirtualAssistent.py      ← Input only (type or voice), no menu
```

---

## How the Layers Communicate

```
main.py
  ├── VirtualAssistent          (UI — input only)
  ├── AssistentController       (routing via intent)
  └── register_all_handlers()   (wiring)
          │
          ├── IntentDetector    (classifies every input)
          │
          ├── QuestionHandler
          │     ├── LLMClient   (shared conversation memory)
          │     └── VoiceOutput (speaks replies via Edge TTS)
          │
          └── MusicHandler
                ├── LLMClient   (extracts best YouTube search query)
                └── pywhatkit   (plays on YouTube)

VirtualAssistent
  └── VoiceInput                (microphone listening)
```

---

## Class Reference

### `main.py`
**Responsibility:** Boot the app. Never changes.
- Loads `.env` before any imports
- Creates `VirtualAssistent` and `AssistentController`
- Calls `register_all_handlers()`
- Runs the async event loop

---

### `src/UI/VirtualAssistent.py` — `VirtualAssistent`
**Responsibility:** Input only — typed or voice. No menu, no logic, no routing.
- `get_input()` — async method, returns user input as string or None
- Type `v` → enables voice mode (stays on)
- Say `bye bye` → disables voice mode, back to typing
- `voice_mode` — read-only property handlers use to decide text vs voice response

---

### `src/Core/AssistentController.py` — `AssistentController`
**Responsibility:** Main loop and intent-based routing. Never changes.
- `register(mode, handler)` — registers a `BaseHandler` for a given mode
- `run()` — main while loop, gets input, detects intent, calls handler
- Owns `IntentDetector` instance

---

### `src/Core/Handlers/BaseHandler.py` — `BaseHandler` *(abstract)*
**Responsibility:** Contract all handlers must follow.
- Every handler inherits this and implements `async handle(user_input: str)`
- Stores `self.ui` reference to `VirtualAssistent`

---

### `src/Core/Handlers/QuestionHandler.py` — `QuestionHandler`
**Responsibility:** Handles Q&A — receives input, responds in text or voice.
- `handle(user_input)` — routes to text or voice response based on `ui.voice_mode`
- `_respond_text()` — streams LLM reply word by word to terminal
- `_respond_voice()` — gets full LLM reply, prints and speaks via `VoiceOutput`
- Receives shared `LLMClient` via injection — conversation memory persists across sessions

---

### `src/Core/Handlers/MusicHandler.py` — `MusicHandler`
**Responsibility:** Handles music — extracts best search query then plays it.
- `handle(user_input)` — sends natural language to dedicated LLM, gets clean YouTube query back
- Owns its own `LLMClient` with a music-focused system prompt
- Uses `pywhatkit.playonyt()` to play the result on YouTube

---

### `src/Core/Handlers/registry.py` — `register_all_handlers()`
**Responsibility:** The ONLY place that connects modes to handler instances.
- Creates one shared `LLMClient` for conversation memory
- Registers all handlers with the controller
- Only file that changes when adding a new feature

---

### `src/Services/AIModelsApi.py` — `LLMClient`
**Responsibility:** Reusable OpenRouter API wrapper with memory and fallback chain.
- Tries 5 free models in order, best conversational quality first:
  1. `arcee-ai/trinity-large-preview:free`
  2. `meta-llama/llama-4-maverick:free`
  3. `deepseek/deepseek-chat-v3-0324:free`
  4. `deepseek/deepseek-r1:free`
  5. `openrouter/free` (guaranteed fallback)
- Auto-falls back on 400, 404, 429 errors
- `chat(input)` — returns full response, keeps history
- `chat_stream(input)` — streams response word by word
- `reset()` — clears conversation history
- `history` — read-only property of full conversation
- System prompt tells model to respond conversationally (no markdown/bullets)

---

### `src/Services/IntentDetector.py` — `IntentDetector`
**Responsibility:** Classify every user input into a mode. Never chats, only classifies.
- `detect(user_input)` — returns an `AssistentTypeSolicitude` enum value
- Uses its own dedicated `LLMClient` with a classification-only system prompt
- Completely isolated from conversation history
- Returns `QUESTIONS` as default fallback if label is unrecognized

---

### `src/Services/VoiceInput.py` — `VoiceInput`
**Responsibility:** Microphone → text via Google Speech Recognition (free, needs internet).
- `listen()` — listens up to 5s for speech start, 10s max phrase length
- Returns transcribed string or `None` if nothing understood
- Used by `VirtualAssistent.get_input()` when voice mode is active

---

### `src/Services/VoiceOutput.py` — `VoiceOutput`
**Responsibility:** Text → speech via Microsoft Edge TTS neural voices (free, needs internet).
- `async speak(text)` — generates mp3 via Edge TTS and plays via pygame
- Default voice: `en-US-AriaNeural` (natural female, Cortana-like)
- Other voices: `en-US-JennyNeural`, `en-US-GuyNeural`, `en-GB-SoniaNeural`
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

## Three LLM Instances — Why

```
LLMClient (conversation)   → QuestionHandler  — remembers full chat history
LLMClient (intent)         → IntentDetector   — classifies only, no history pollution
LLMClient (music)          → MusicHandler     — extracts YouTube queries only
```
Each instance is focused on one job with its own system prompt and isolated history.

---

## Voice Mode Flow

```
User types 'v'
  → voice mode ON
  → VoiceInput.listen() called for each input
  → QuestionHandler._respond_voice() used instead of _respond_text()
  → LLMClient.chat() gets full reply
  → VoiceOutput.speak() reads it out loud via Edge TTS Aria
  → listens again automatically

User says 'bye bye'
  → voice mode OFF → back to typing

User says/types 'exit'
  → IntentDetector returns EXIT → app closes
```

---

## Adding a New Feature

Example — adding a weather feature:

```
1. src/Types/AssistentTypeSolicitude.py
   → Add: WEATHER = 4

2. src/Services/IntentDetector.py
   → Add to system prompt:
     "WEATHER — the user wants to know the weather for a city"
   → Add to detect(): elif "WEATHER" in label: return mode.WEATHER

3. src/Core/Handlers/WeatherHandler.py  ← create this file
   from src.Core.Handlers.BaseHandler import BaseHandler

   class WeatherHandler(BaseHandler):
       async def handle(self, user_input: str) -> None:
           # your weather logic here
           print("Getting weather...")

4. src/Core/Handlers/registry.py
   → from src.Core.Handlers.WeatherHandler import WeatherHandler
   → controller.register(mode.WEATHER, WeatherHandler(ui))
```

`main.py`, `AssistentController`, `BaseHandler`, `VirtualAssistent`, `LLMClient` — never touched.