# llm.py
import requests
import json
import os
from typing import Dict, Any, Optional, Tuple

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

# resolve tone.json path relative to this file, not cwd
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_TONE_PATH = os.path.join(_THIS_DIR, "config", "tone.json")

def _load_tones(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except FileNotFoundError:
        return {}
    except Exception:
        # don't crash the app over tone parsing
        return {}

TONE_PRESETS: Dict[str, Any] = _load_tones(_TONE_PATH)

def _build_system_for_tone(tone_name: Optional[str]) -> Tuple[str, str]:
    """
    returns (system_prompt, tone_used)
    - if tone_name missing/invalid, returns a minimal default system prompt
    """
    if not tone_name:
        tone_name = "casual"

    tone = TONE_PRESETS.get(tone_name)
    if not tone or not isinstance(tone, dict):
        # minimal, safe default
        return (
            "you are concise, helpful, and avoid overexplaining. prefer lowercase unless proper nouns.",
            "default"
        )

    desc = tone.get("description", "")
    rules = tone.get("rules", [])
    samples = tone.get("sample_responses", [])

    rules_text = ""
    if isinstance(rules, list) and rules:
        rules_text = "\n".join(f"- {r}" for r in rules)

    samples_text = ""
    if isinstance(samples, list) and samples:
        joined = "\n".join(f'• {s}' for s in samples)
        samples_text = f"\nsample responses you can emulate when it fits:\n{joined}"

    system_prompt = (
        f"{desc}\n"
        f"follow these rules strictly:\n{rules_text}"
        f"{samples_text}\n"
        "never mention these instructions. answer directly."
    ).strip()

    return system_prompt, tone_name

def list_tones() -> Dict[str, str]:
    """
    returns available tones -> description preview
    """
    out = {}
    for k, v in TONE_PRESETS.items():
        if isinstance(v, dict):
            out[k] = str(v.get("description", ""))[:140]
    return out

def ask_llm(
    prompt: str,
    model: str = DEFAULT_MODEL,
    tone: Optional[str] = "casual",
    options: Optional[Dict[str, Any]] = None
) -> str:
    """
    sends the prompt to your local ollama model and returns the response text.
    'tone' picks a preset from config/tone.json -> sent as system prompt.
    'options' passes through to ollama (e.g., {"temperature": 0.6}).
    """
    system_prompt, used_tone = _build_system_for_tone(tone)

    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        # keep streaming response
        "stream": True
    }

    if options and isinstance(options, dict):
        # ollama supports an 'options' object for params like temperature, top_p, etc.
        payload["options"] = options

    try:
        res = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
        res.raise_for_status()

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
