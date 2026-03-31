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
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "mistral:latest",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    yield data["message"]["content"]
            except:
                continue