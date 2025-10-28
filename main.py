from speech_to_text import get_user_text
from llm import ask_llm
from text_to_speech import speak
from commands import handle_command
from logger import log_event

def main():
    print("cosync online. type 'exit' to quit.\n")

    while True:
        user_text = get_user_text()

        if user_text is None:
            continue

        cleaned = user_text.strip()

        if cleaned.lower() == "exit":
            print("cosync: shutting down. later.")
            # optional: log shutdown
            log_event("system", {
                "action": "shutdown",
                "note": "user exited session"
            })
            break

        # 1. try to handle as local command
        command_result = handle_command(cleaned)

        if command_result is not None:
            speak(command_result)

            # log this command run
            log_event("command", {
                "input": cleaned,
                "output": command_result,
                "handler": "handle_command"
            })

            continue

        # 2. fallback to llm
        llm_reply = ask_llm(cleaned)
        speak(llm_reply)

        # log llm response
        log_event("llm", {
            "input": cleaned,
            "output": llm_reply,
            "model": "placeholder"
        })

if __name__ == "__main__":
    main()