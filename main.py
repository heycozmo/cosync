# main.py
from llm import ask_llm
from commands import handle_command
from logger import log_event
from text_to_speech import speak

# --- simple routing helpers ---

def pick_tone(intent: str) -> str:
    """
    map high-level intent -> tone.json key
    available today: "casual", "working"
    """
    if intent == "execute":
        return "working"
    # default for chat/explain/etc.
    return "casual"

def classify_intent(user_text: str) -> str:
    """
    super lightweight, no extra llm call:
    - if it's a question or asks for explanation -> "chat"
    - otherwise still "chat" since commands are already caught earlier
    """
    t = user_text.strip().lower()
    question_words = ("why", "how", "what", "when", "where", "who", "which", "explain", "help", "can you")
    if t.endswith("?") or any(t.startswith(w) for w in question_words):
        return "chat"
    return "chat"

def pick_ollama_options(tone: str) -> dict:
    """
    dial generation behavior by tone.
    """
    if tone == "working":
        return {"temperature": 0.3, "top_p": 0.9, "repeat_penalty": 1.1}
    # casual default
    return {"temperature": 0.5, "top_p": 0.9, "repeat_penalty": 1.08}

def safe_speak(text: str):
    """
    guard tts so a bad synth call doesn't crash the loop.
    """
    try:
        speak(text)
    except Exception as e:
        print(f"[tts error: {e}]")
        # last resort: print to console
        print(f"cosync: {text}")

def get_user_text():
    return input("you: ")

def main():
    safe_speak("cosync online. type 'exit' to quit.")

    while True:
        user_text = get_user_text()
        if not user_text:
            continue

        cleaned = user_text.strip()

        # exit path
        if cleaned.lower() == "exit":
            safe_speak("shutting down. later.")
            log_event("system", {
                "action": "shutdown",
                "note": "user exited session"
            })
            break

        # 1) try direct command first (spotify, system status, etc.)
        command_result, handler_name = handle_command(cleaned)

        if command_result is not None:
            safe_speak(command_result)
            log_event("command", {
                "input": cleaned,
                "output": command_result,
                "handler": handler_name
            })
            continue

        # 2) fallback to llm (non-command)
        intent = classify_intent(cleaned)         # "chat" for now
        tone = pick_tone("execute" if handler_name else intent)  # if you later route "execute" intents, tone becomes "working"
        options = pick_ollama_options(tone)

        llm_reply = ask_llm(cleaned, tone=tone, options=options)
        safe_speak(llm_reply)

        log_event("llm", {
            "input": cleaned,
            "output": llm_reply,
            "model": "llama3",
            "tone": tone,
            "options": options
        })

if __name__ == "__main__":
    main()