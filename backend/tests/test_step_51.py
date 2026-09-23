from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.step_51 import TOOL_DEFS, TOOL_REGISTRY, run_agent


def test_tool_defs_count():
    assert len(TOOL_DEFS) == 9


def test_tool_defs_names():
    names = [t["function"]["name"] for t in TOOL_DEFS]
    expected = [
        "read_file", "list_dir", "search_files",
        "detect_project_type", "find_dependencies",
        "find_ci_cd_configs", "find_secret_files",
        "get_plan", "write_result",
    ]
    assert names == expected


def test_tool_registry_complete():
    for tool_def in TOOL_DEFS:
        name = tool_def["function"]["name"]
        assert name in TOOL_REGISTRY, f"missing: {name}"


@pytest.mark.asyncio
async def test_run_agent_mocked():
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "# Результат анализа"
    mock_choice.message.tool_calls = None
    mock_choice.finish_reason = "stop"
    mock_completion.choices = [mock_choice]

    with patch("app.services.llm._get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
        mock_get_client.return_value = mock_client

        result = await run_agent("/fake/repo/path")

    assert "# Результат анализа" in result
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_run_agent_tool_loop():
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = ""
    mock_tc = MagicMock()
    mock_tc.id = "call_1"
    mock_tc.function.name = "read_file"
    mock_tc.function.arguments = '{"path": "/test"}'
    mock_choice.message.tool_calls = [mock_tc]
    mock_choice.finish_reason = "tool_calls"
    mock_completion.choices = [mock_choice]

    mock_completion2 = MagicMock()
    mock_choice2 = MagicMock()
    mock_choice2.message.content = "# Итоговый результат"
    mock_choice2.message.tool_calls = None
    mock_choice2.finish_reason = "stop"
    mock_completion2.choices = [mock_choice2]

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[mock_completion, mock_completion2],
    )

    with patch("app.services.llm._get_client") as mock_get_client:
        mock_get_client.return_value = mock_client

        result = await run_agent("/fake/repo/path")

    assert "# Итоговый результат" in result
    assert mock_client.chat.completions.create.call_count == 2
