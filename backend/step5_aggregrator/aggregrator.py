from crewai import Crew
from .crew_tasks import create_aggregation_task


def aggregate_agent_outputs(agent_results):

    task = create_aggregation_task(agent_results)

    crew = Crew(
        agents=[task.agent],
        tasks=[task],
        verbose=True
    )

    try:
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        print("AGGREGATOR SKIPPED:", e)
        parts = []
        for item in agent_results or []:
            name = item.get("agent_name", "agent")
            parts.append(f"{name}: {item.get('analysis', '')}")
        return "\n\n".join(parts) or f"Could not aggregate agent output. {e}"