def ask_llm(prompt: str) -> str:
    """
    placeholder brain.
    later this will call the real model.
    for now it's not.
    """

    # tune this voice however later
    return (
        "you said: '"
        + prompt
        + "'. i'm answering with the placeholder model right now. i'll get upgraded soon."
    )