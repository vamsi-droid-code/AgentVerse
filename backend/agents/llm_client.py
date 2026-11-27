import os
import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")


def call_llm(system_prompt: str, user_input: str):

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5
    }

    response = requests.post(
        f"{OLLAMA_BASE_URL}/v1/chat/completions",
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        detail = response.text[:240]
        return (
            "The local model did not return an answer "
            f"({response.status_code}). {detail}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"]
