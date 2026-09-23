from unittest.mock import AsyncMock, patch

from app.graph.state_graph import AgentState, get_graph


def test_agent_state_fields():
    state: AgentState = {
        "session_id": "test",
        "repo_path": "/fake/repo",
        "messages": [],
        "result": None,
        "error": None,
    }
    assert state["session_id"] == "test"
    assert state["repo_path"] == "/fake/repo"


def test_get_graph_returns_compiled():
    graph = get_graph()
    assert graph is not None


async def test_graph_analyze_node():
    graph = get_graph()
    with patch(
        "app.graph.state_graph.run_agent",
        new=AsyncMock(return_value="# Test result"),
    ):
        result = await graph.ainvoke({
            "session_id": "test",
            "repo_path": "/fake/repo",
            "messages": [],
        })
        assert result["result"] == "# Test result"
        assert result["error"] is None


async def test_graph_analyze_node_error():
    graph = get_graph()
    with patch(
        "app.graph.state_graph.run_agent",
        new=AsyncMock(side_effect=ValueError("test error")),
    ):
        result = await graph.ainvoke({
            "session_id": "test",
            "repo_path": "/fake/repo",
            "messages": [],
        })
        assert result["result"] is None
        assert result["error"] == "test error"


def test_graph_analyze_node_sync():
    graph = get_graph()
    with patch(
        "app.graph.state_graph.run_agent",
        new=AsyncMock(return_value="# Test result"),
    ):
        result = __import__("asyncio").run(
            graph.ainvoke({
                "session_id": "test",
                "repo_path": "/fake/repo",
                "messages": [],
            })
        )
        assert result["result"] == "# Test result"
        assert result["error"] is None
