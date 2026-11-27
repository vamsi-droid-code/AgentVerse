import os
import requests
import json

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")


SYSTEM_PROMPT = """
You are an AI system that analyzes a user's idea
and decides which specialized agents are needed.

Return STRICT JSON only.

Example:
{
    "intent": "idea_analysis",
    "agents": ["idea_clarity_agent", "market_agent", "risk_agent"]
}
"""

def ai_route_decision(message: str) -> dict:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/v1/chat/completions",
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return fallback_decision(
                message,
                reason=f"Ollama error {response.status_code}"
            )

        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.strip("`")
            if content.lower().startswith("json"):
                content = content[4:]
            content = content.strip()

        return json.loads(content)

    except Exception as e:
        return fallback_decision(message, reason=str(e))


def fallback_decision(message: str, reason: str) -> dict:
    """
    Safe fallback if LLM fails
    """
    return {
        "intent": "general_query",
        "agents": ["general_agent"],
        "fallback": True,
        "reason": reason
    }
