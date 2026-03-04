# 🤖 Cortana — Virtual Assistant

A Python-based virtual assistant powered by free LLMs via [OpenRouter](https://openrouter.ai/). Supports natural language Q&A and YouTube music playback, with a clean architecture designed to scale toward a React frontend.

---

## 📁 Project Structure

```
Virtual_assistent/
│   .env                        ← API keys (never commit this)
│   main.py                     ← Entry point
│
└───src/
    ├───Core/
    │       AssistentController.py   ← Main loop and conversation flow
    │       AssistentModes.py        ← Actions (LLM calls, music playback)
    │
    ├───Models/
    │       AIModelsApi.py           ← LLMClient — reusable OpenRouter wrapper
    │       User.py                  ← User input model
    │
    ├───Types/
    │       AssistentTypeSolicitude.py  ← Enum for assistant modes
    │
    └───UI/
            VirtualAssistent.py      ← Terminal UI (menus, prompts)
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Virtual_assistent.git
cd Virtual_assistent
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install openai python-dotenv pywhatkit
```

### 4. Set up your API key
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```
Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys).

---

## 🚀 Running the Assistant

```bash
python main.py
```

```
Cortana is starting up...

Hello! My name is Cortana, I'm here to help you.
What do you want to do?
  1. Ask a question
  2. Play a song
  3. Exit

Choose an option: 1

Ask me anything! Type 'back' to return to the menu.

You: Who is LeBron James?
Assistant: LeBron James is a professional basketball player...

You: back
```

---

## 🧠 How It Works

```
main.py
  └── AssistentController     ← controls the flow
        ├── VirtualAssistent  ← handles all terminal UI
        └── AssistentModes    ← executes actions
              └── LLMClient   ← talks to OpenRouter API
```

- **Questions** → sent to OpenRouter's free LLM tier, streamed back word by word
- **Music** → searched and played on YouTube via `pywhatkit`
- **Conversation memory** → the LLMClient keeps history within a session so the assistant remembers context

---

## 🔌 LLMClient — Reusable API Wrapper

The `LLMClient` class in `src/Models/AIModelsApi.py` can be used independently anywhere in the project:

```python
from src.Services.AIModelsApi import LLMClient

llm = LLMClient()
reply = await llm.chat("What is Python?")  # returns string
await llm.chat_stream("Tell me a joke")  # streams to stdout

llm = LLMClient(system_prompt="You are a chef.")  # custom persona
llm.reset()  # clear history
```

---

## 🗺️ Roadmap

- [x] Natural language Q&A via LLM
- [x] YouTube music playback
- [x] Conversation memory within session
- [ ] FastAPI backend for React frontend
- [ ] Voice input / output
- [ ] Weather lookup
- [ ] Reminders and timers

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `openai` | OpenAI-compatible client for OpenRouter |
| `python-dotenv` | Load API keys from `.env` |
| `pywhatkit` | YouTube music playback |

---

## ⚠️ Notes

- The free OpenRouter tier has rate limits (~200 requests/day). If you hit them, wait a few minutes and try again.
- Never commit your `.env` file. Make sure `.env` is in your `.gitignore`.