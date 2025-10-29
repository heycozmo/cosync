import pyttsx3

def speak(text: str):
    print(f"cosync: {text}")

    try:
        engine = pyttsx3.init()
        # optional tweaks:
        # rate = engine.getProperty('rate')
        # engine.setProperty('rate', rate - 20)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print(f"[tts error: {e}]")