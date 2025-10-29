<div align="center">
  <h1>🧠 cosync</h1>
  <p><strong>local ai assistant built to think, speak, and act — your personal jarvis, powered by ollama.</strong></p>
  <img src="https://img.shields.io/badge/version-v1.0--alpha-blue.svg" alt="version badge">
  <img src="https://img.shields.io/badge/python-3.10+-yellow.svg" alt="python version">
  <img src="https://img.shields.io/badge/status-active-success.svg" alt="status badge">
</div>

---

## 🚀 overview

**cosync** is a locally hosted ai assistant that runs directly on your pc — no external servers, no data sharing.  
it listens, speaks, and performs actions through modular tools like spotify control, logging, and local llm reasoning.

its goal: to feel *alive* on your system — capable of reacting, remembering, and assisting, just like a real digital companion.

---

## 🧩 current version — v1 (core loop)

### ✅ features
- 🧠 local llm integration — connects to [ollama](https://ollama.ai/) (llama3 by default)
- 🔀 command routing — routes between user intent (commands vs. questions)
- 🎵 spotify control — play, pause, skip, get track info
- 🔊 text-to-speech — offline voice output via pyttsx3
- 🧾 logging system — structured jsonl event logs
- ⚙️ modular design — extendable for future systems (pulse, memory, dashboard, etc.)

### 🗂 folder structure
cosync/
│
├── main.py               # core loop (routing + input/output)
├── llm.py                # handles local ollama prompts
├── commands.py           # command detection + dispatch
├── spotify_control.py    # spotify connect actions
├── text_to_speech.py     # voice output (pyttsx3)
├── speech_to_text.py     # placeholder for future mic input
├── logger.py             # jsonl logging system
└── README.md

---

## 🧭 roadmap

### 🩵 v1 — local assistant core
- [x] local llm (ollama llama3)
- [x] core routing
- [x] spotify control
- [x] tts voice output
- [ ] stt input
- [ ] memory system
- [ ] pulse diagnostic system
- [ ] localhost dashboard
- [ ] safety / confirmation layer

### 🩶 v2 — remote access & context
- 🌐 use anywhere via email or api calls  
- 🔐 voice id + passcode for secure access  
- 🕵️ proactive “pulse” context awareness  
- 📱 device sync + presence detection  

### 🩵 v3 — autonomous companion
- 💬 conversational awareness (follow-ups, context memory)
- ⚙️ proactive behavior (initiate convos, give updates)
- 🖥️ full dashboard with activity timeline + insights
- 🤖 task automation (order food, send messages, etc.)

---

## 🛠 setup

### prerequisites
- python 3.10+
- [ollama](https://ollama.ai/) installed and running locally  
- spotify developer app (client id + secret)
- required python libs:
  pip install requests spotipy pyttsx3 psutil

### running cosync
ollama serve
python main.py

---

## 💬 example interaction
you: pause the music  
cosync: paused spotify.

you: what are you  
cosync: i am llama3, a local ai model trained to assist and converse naturally.

---

## 🧠 about
cosync is built by **cos** as a long-term personal ai project — designed for privacy, customization, and local control.  
it’s an ongoing experiment to merge llms, automation, and real-world utility into a single, self-contained system.

> "cosync isn't just an assistant — it's a local ecosystem."

---

<div align="center">
  <sub>built with 🧠, ☕, and a bit of chaos • 2025</sub>
</div>