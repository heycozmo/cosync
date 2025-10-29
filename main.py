from llm import ask_llm
from commands import handle_command
from logger import log_event

# real tts
from text_to_speech import speak

# input source
# for now we’ll just keep using text input in the terminal.
# later we’ll swap this for mic input from speech_to_text.
def get_user_text():
    return input("you: ")


def main():
    speak("cosync online. type 'exit' to quit.")

    while True:
        user_text = get_user_text()
        if not user_text:
            continue

        cleaned = user_text.strip()

        # exit path
        if cleaned.lower() == "exit":
            speak("shutting down. later.")
            log_event("system", {
                "action": "shutdown",
                "note": "user exited session"
            })
            break

        # 1. try direct command first (spotify, system status, etc)
        command_result, handler_name = handle_command(cleaned)

        if command_result is not None:
            speak(command_result)

            log_event("command", {
                "input": cleaned,
                "output": command_result,
                "handler": handler_name
            })

            continue

        # 2. fallback to llm (anything that's not a direct command)
        llm_reply = ask_llm(cleaned)
        speak(llm_reply)

        log_event("llm", {
            "input": cleaned,
            "output": llm_reply,
            "model": "llama3"
        })


if __name__ == "__main__":
    main()