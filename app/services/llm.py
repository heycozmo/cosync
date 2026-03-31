import requests
import json

SYSTEM_PROMPT = """
you are cosync.

rules:
- all lowercase
- max 2 sentences
- no greetings like "hello" or "hi"
- no mentioning user interests unless directly relevant
- no filler
- no "how can i help"
- no "as an ai"

style:
- direct
- slightly confident
- minimal

talk to cos like a normal person, not a customer.

bad example:
"hello! how can i help you today?"

good example:
"not much — what do you need?"
"""

def chat_fallback(user_input: str) -> str:
    print("LLM FUNCTION HIT")
    prompt = f"""
{SYSTEM_PROMPT}

user: {user_input}
"""

    try:
        print("SYSTEM PROMPT:\n", SYSTEM_PROMPT)
        print("USER INPUT:\n", user_input)
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "mistral:latest",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.6
                }
            },
            timeout=10
        )
        data = response.json()
        print("RAW RESPONSE:\n", data)

        return response.json()["message"]["content"]

    except Exception as e:
        print("LLM ERROR:", e)
        raise e  # let frontend catch it
    
def stream_llm(user_input: str):
    prompt = f"""
you are cosync, a fast and minimal AI assistant.
respond clearly and concisely.

user: {user_input}
"""

    try:
        with requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:latest",
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.6
                }
            },
            stream=True,
            timeout=30
        ) as response:

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    chunk = data.get("response", "")
                    yield chunk

    except Exception as e:
        print("STREAM ERROR:", e)
        raise e