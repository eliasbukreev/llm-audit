from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.step_51 import run_agent


class AgentState(TypedDict):
    session_id: str
    repo_path: str
    messages: list[dict]
    result: str | None
    error: str | None


async def _analyze_node(state: AgentState) -> dict:
    try:
        result = await run_agent(state["repo_path"])
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}


def get_graph():
    builder = StateGraph(AgentState)
    builder.add_node("analyze", _analyze_node)
    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", END)
    # builder.add_edge("analyze", "5.3")
    # builder.add_edge("analyze", "5.4")
    # builder.add_edge("analyze", "5.5")
    # builder.add_edge("5.3", "5.6")
    # builder.add_edge("5.4", "5.6")
    # builder.add_edge("5.5", "5.6")
    # builder.add_edge("5.6", END)
    return builder.compile(checkpointer=False)
