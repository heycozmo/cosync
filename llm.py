def ask_llm(prompt: str) -> str:
    """
    placeholder brain.
    later:
    - send `prompt` to a local model or api
    - get actual response
    """
    # dumb example logic just so it feels alive
    if "cpu" in prompt.lower():
        return "i can't read system stats yet, but that'll be part of system status in v1."
    if "who are you" in prompt.lower():
        return "i'm cosync. i'm running locally and i'm here to make your life easier."

    return f"i heard you say: '{prompt}'. i'll get smarter once you hook up the real model."