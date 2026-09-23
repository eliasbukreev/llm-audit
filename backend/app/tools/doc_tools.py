import subprocess
from pathlib import Path

from app.config import settings


def get_plan(step: str) -> str:
    plan_map = {
        "5.1": "Анализ текущего состояния процессов разработки безопасного ПО",
        "5.3": "Регламент управления требованиями безопасности (п.5.3 ГОСТ)",
        "5.4": "Регламент управления конфигурацией ПО (п.5.4 ГОСТ)",
        "5.5": "Регламент управления недостатками и запросами на изменение (п.5.5 ГОСТ)",
        "5.6": "Описание архитектуры ПО (п.5.6 ГОСТ)",
    }

    filename = plan_map.get(step)
    if not filename:
        return f"ERROR: unknown step: {step}"

    plan_path = settings.docs_dir / "plans" / f"{filename}.md"
    if not plan_path.exists():
        return f"ERROR: plan not found: {plan_path}"
    return plan_path.read_text(encoding="utf-8")


def write_result(path: str, content: str) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.write_text(content, encoding="utf-8")
        return f"OK: written to {target}"
    except Exception as e:
        return f"ERROR: {e}"


def convert_to_docx(input_path: str, output_path: str) -> str:
    try:
        result = subprocess.run(
            ["pandoc", input_path, "-o", output_path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return f"ERROR: pandoc failed: {result.stderr}"
        return output_path
    except FileNotFoundError:
        return "ERROR: pandoc not found"
    except subprocess.TimeoutExpired:
        return "ERROR: pandoc timed out"
