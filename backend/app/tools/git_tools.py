import re
import subprocess
from pathlib import Path

from app.config import settings


def git_clone(url: str, dest: str = "") -> str:
    repos_path = settings.repos_dir
    repos_path.mkdir(parents=True, exist_ok=True)

    if dest:
        target = repos_path / dest
    else:
        name = re.search(r"/([^/]+?)(?:\.git)?$", url)
        target = repos_path / (name.group(1) if name else "repo")

    if target.exists():
        return f"ERROR: already exists: {target}"

    try:
        subprocess.run(
            ["git", "clone", url, str(target)],
            capture_output=True,
            text=True,
            timeout=300,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        return f"ERROR: git clone failed: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "ERROR: git clone timed out after 300s"
    except FileNotFoundError:
        return "ERROR: git not found"
    return str(target)


def get_structure(path: str, depth: int = 3) -> str:
    base = Path(path)
    if not base.is_dir():
        return f"ERROR: not a directory: {base}"

    lines = [f"📁 {base.name}/"]

    def _walk(current: Path, indent: int, current_depth: int):
        if current_depth >= depth:
            return
        entries = sorted(current.iterdir())
        for entry in entries:
            if entry.name.startswith("."):
                continue
            prefix = "  " * (indent + 1)
            if entry.is_dir():
                lines.append(f"{prefix}📁 {entry.name}/")
                _walk(entry, indent + 1, current_depth + 1)
            else:
                lines.append(f"{prefix}📄 {entry.name}")

    _walk(base, 0, 0)
    return "\n".join(lines)


def get_history(path: str, limit: int = 10) -> list[dict]:
    try:
        base = Path(path).resolve()
        repos_root = settings.repos_dir.resolve()
        if repos_root not in base.parents and base != repos_root:
            return [{"error": f"path outside repos_dir: {base}"}]
    except Exception as e:
        return [{"error": str(e)}]

    try:
        result = subprocess.run(
            ["git", "log", "--oneline", f"-{limit}", "--format=%h %ci %s"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return [{"error": result.stderr}]
        commits = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    commits.append({
                        "hash": parts[0],
                        "date": parts[1],
                        "message": parts[2],
                    })
        return commits
    except subprocess.TimeoutExpired:
        return [{"error": "git log timed out"}]
    except FileNotFoundError:
        return [{"error": "git not found"}]
