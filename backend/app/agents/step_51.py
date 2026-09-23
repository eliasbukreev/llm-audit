import json
from collections.abc import Callable

from app.services.llm import build_messages, chat_completion
from app.tools import doc_tools, filesystem, project_tools

TOOL_DEFS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads a file and returns its full contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "Lists files and directories in a given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the directory"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Searches for files by name pattern in a directory tree.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "File name pattern"},
                    "path": {"type": "string", "description": "Root directory to search in"},
                },
                "required": ["pattern", "path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "detect_project_type",
            "description": "Detects the primary programming language/framework of a project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the project directory"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_dependencies",
            "description": "Finds and reads dependency files in a project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the project directory"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_ci_cd_configs",
            "description": "Finds CI/CD configuration files in a project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the project directory"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_secret_files",
            "description": "Finds potential secret or credential files in a project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the project directory"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_plan",
            "description": "Retrieves the analysis plan for a given step (e.g. '5.1').",
            "parameters": {
                "type": "object",
                "properties": {
                    "step": {"type": "string", "description": "Step identifier (e.g. '5.1')"},
                },
                "required": ["step"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_result",
            "description": "Writes analysis result content to a file in results directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Full path to write the result to"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
]

TOOL_REGISTRY: dict[str, Callable[..., object]] = {
    "read_file": filesystem.read_file,
    "list_dir": filesystem.list_dir,
    "search_files": filesystem.search_files,
    "detect_project_type": project_tools.detect_project_type,
    "find_dependencies": project_tools.find_dependencies,
    "find_ci_cd_configs": project_tools.find_ci_cd_configs,
    "find_secret_files": project_tools.find_secret_files,
    "get_plan": doc_tools.get_plan,
    "write_result": doc_tools.write_result,
}


async def run_agent(repo_path: str) -> str:
    plan = doc_tools.get_plan("5.1")
    user_input = (
        f"Проанализируй репозиторий по пути {repo_path}.\n"
        f"Вот план анализа для шага 5.1:\n{plan}"
    )
    messages = build_messages(plan, user_input)

    for _ in range(15):
        result = await chat_completion(messages, tools=TOOL_DEFS)

        assistant_msg: dict = {"role": "assistant", "content": result["content"]}
        if result["tool_calls"]:
            assistant_msg["tool_calls"] = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]},
                }
                for tc in result["tool_calls"]
            ]
        messages.append(assistant_msg)

        if not result["tool_calls"]:
            return result["content"]

        for tc in result["tool_calls"]:
            tool_name = tc["name"]
            try:
                args = json.loads(tc["arguments"]) if tc["arguments"] else {}
                func = TOOL_REGISTRY[tool_name]
                raw = func(**args)
                if isinstance(raw, list):
                    tool_result = "\n".join(str(item) for item in raw)
                else:
                    tool_result = str(raw)
            except KeyError:
                tool_result = f"ERROR: unknown tool: {tool_name}"
            except Exception as e:
                tool_result = f"ERROR: {e}"

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": tool_result,
            })

    return "Максимальное количество итераций достигнуто."
