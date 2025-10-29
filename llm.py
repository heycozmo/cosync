# llm.py
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

def ask_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    sends the prompt to your local ollama model and returns the response text.
    """
    payload = {
        "model": model,
        "prompt": prompt
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, stream=True)
        res.raise_for_status()  # raises if the API returns an error

        response_text = ""
        for line in res.iter_lines():
            if not line:
                continue
            data = json.loads(line)
            if "response" in data:
                response_text += data["response"]
            if data.get("done"):
                break

        return response_text.strip() if response_text else "[no response]"

    except requests.exceptions.RequestException as e:
        return f"[network error: {e}]"
    except json.JSONDecodeError:
        return "[error: invalid json from ollama]"
    except Exception as e:
        return f"[unexpected error: {e}]"
