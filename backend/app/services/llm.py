from openai import AsyncOpenAI

from app.config import settings

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_api_url,
        )
    return _client


def build_messages(system_prompt: str, user_input: str) -> list[dict]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]


async def chat_completion(messages: list[dict], tools: list[dict] | None = None) -> dict:
    kwargs: dict = {"messages": messages}
    if tools:
        kwargs["tools"] = tools
    response = await _get_client().chat.completions.create(
        model=settings.llm_model,
        **kwargs,
    )
    choice = response.choices[0]
    message = choice.message
    return {
        "content": message.content or "",
        "tool_calls": [
            {
                "id": tc.id,
                "name": tc.function.name,
                "arguments": tc.function.arguments,
            }
            for tc in (message.tool_calls or [])
        ],
        "finish_reason": choice.finish_reason,
    }
