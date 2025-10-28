from speech_to_text import get_user_text
from llm import ask_llm
from text_to_speech import speak
from commands import handle_command

def main():
    print("cosync online. type 'exit' to quit.\n")

    while True:
        user_text = get_user_text()

        if user_text is None:
            # if stt fails in the future we just loop again
            continue

        cleaned = user_text.strip()
        if cleaned.lower() == "exit":
            print("cosync: shutting down. later.")
            break

        # 1. try to handle it as a local command
        command_result = handle_command(cleaned)

        if command_result is not None:
            # local action handled it
            speak(command_result)
            continue

        # 2. not a local command -> send to llm
        llm_reply = ask_llm(cleaned)
        speak(llm_reply)

if __name__ == "__main__":
    main()