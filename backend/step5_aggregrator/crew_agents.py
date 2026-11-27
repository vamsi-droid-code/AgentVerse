import os
from crewai import Agent, LLM

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")

llm = LLM(
    model=OLLAMA_MODEL,
    base_url=f"{OLLAMA_BASE_URL}/v1",
    api_key="ollama",
    custom_openai=True,
    temperature=0.7
)

aggregator_agent = Agent(
    role="Aggregation Specialist",
    goal="Combine outputs from different agents into one final report",
    backstory="Expert AI analyst skilled at merging insights from multiple sources.",
    llm=llm,
    verbose=True
)
