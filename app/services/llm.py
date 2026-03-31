import requests
import json

def chat_fallback(user_input: str) -> str:
    prompt = f"""
you are cosync, a fast and minimal AI assistant.
respond clearly and concisely.

user: {user_input}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:latest",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.6
                }
            },
            timeout=10
        )

        return response.json()["response"]

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