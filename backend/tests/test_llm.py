from unittest.mock import AsyncMock, MagicMock

import pytest

from app.config import settings
from app.services.llm import build_messages, chat_completion


def test_build_messages():
    system = "You are an assistant"
    user = "Hello"
    messages = build_messages(system, user)
    assert len(messages) == 2
    assert messages[0] == {"role": "system", "content": system}
    assert messages[1] == {"role": "user", "content": user}


@pytest.mark.asyncio
async def test_chat_completion_with_tools(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Let me check"
    mock_tc = MagicMock()
    mock_tc.id = "call_1"
    mock_tc.function.name = "read_file"
    mock_tc.function.arguments = '{"path": "/test"}'
    mock_choice.message.tool_calls = [mock_tc]
    mock_choice.finish_reason = "tool_calls"
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    monkeypatch.setattr("app.services.llm._get_client", lambda: mock_client)

    messages = build_messages("System prompt", "User input")
    tools = [{"type": "function", "function": {"name": "read_file", "parameters": {}}}]
    result = await chat_completion(messages, tools=tools)

    assert result["content"] == "Let me check"
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["name"] == "read_file"
    assert result["tool_calls"][0]["arguments"] == '{"path": "/test"}'
    assert result["finish_reason"] == "tool_calls"
    mock_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["tools"] == tools
    assert call_kwargs["model"] == settings.llm_model


@pytest.mark.asyncio
async def test_chat_completion_without_tools(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Final answer"
    mock_choice.message.tool_calls = None
    mock_choice.finish_reason = "stop"
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    monkeypatch.setattr("app.services.llm._get_client", lambda: mock_client)

    messages = [{"role": "user", "content": "hi"}]
    result = await chat_completion(messages)

    assert result["content"] == "Final answer"
    assert result["tool_calls"] == []
    assert result["finish_reason"] == "stop"


@pytest.mark.asyncio
async def test_chat_completion_empty_content(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = None
    mock_choice.message.tool_calls = None
    mock_choice.finish_reason = "stop"
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    monkeypatch.setattr("app.services.llm._get_client", lambda: mock_client)

    result = await chat_completion([{"role": "user", "content": "hi"}])
    assert result["content"] == ""