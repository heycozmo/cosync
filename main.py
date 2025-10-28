from speech_to_text import get_user_text
from llm import ask_llm
from text_to_speech import speak

def main():
    print("cosync online. type 'exit' to quit.\n")

    while True:
        user_text = get_user_text()

        if user_text is None:
            # safety check in case stt fails later
            continue

        if user_text.strip().lower() == "exit":
            print("cosync: shutting down. later.")
            break

        # send what you said to the llm
        response = ask_llm(user_text)

        # speak the response (tts stub for now)
        speak(response)

if __name__ == "__main__":
    main()