import os
from pathlib import Path

from app.config import BASE_DIR, settings

ALLOWED_ROOTS = [
    settings.repos_dir,
    settings.docs_dir,
    settings.results_dir,
    BASE_DIR,
]


def _validate(abs_path: Path) -> Path:
    resolved = abs_path.resolve()
    for root in ALLOWED_ROOTS:
        r = root.resolve()
        if r in resolved.parents or resolved == r:
            return resolved
    raise ValueError(f"path outside allowed roots: {resolved}")


def read_file(path: str) -> str:
    try:
        fp = _validate(Path(path))
    except ValueError as e:
        return f"ERROR: {e}"
    if not fp.is_file():
        return f"ERROR: not a file: {fp}"
    try:
        return fp.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"ERROR: {e}"


def list_dir(path: str) -> str:
    try:
        dp = _validate(Path(path))
    except ValueError as e:
        return f"ERROR: {e}"
    if not dp.is_dir():
        return f"ERROR: not a directory: {dp}"
    lines = []
    for entry in sorted(dp.iterdir()):
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            lines.append(f"📁 {entry.name}/")
        else:
            size = entry.stat().st_size
            lines.append(f"📄 {entry.name} ({size}B)")
    return "\n".join(lines) if lines else "(empty directory)"


def search_files(pattern: str, path: str) -> list[str]:
    try:
        base = _validate(Path(path))
    except ValueError as e:
        return [f"ERROR: {e}"]
    results = []
    for root, _dirs, files in os.walk(base):
        for f in files:
            if f.startswith("."):
                continue
            if pattern in f or pattern == "*":
                results.append(str(Path(root) / f))
    return results
