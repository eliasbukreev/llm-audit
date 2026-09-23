import os
from pathlib import Path

PYTHON_SIGNATURES = ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile", "*.py"]
JS_SIGNATURES = ["package.json", "package-lock.json", "*.js", "*.ts", "*.tsx"]
JAVA_SIGNATURES = ["pom.xml", "build.gradle", "*.java"]
GO_SIGNATURES = ["go.mod", "*.go"]
RUST_SIGNATURES = ["Cargo.toml", "*.rs"]
RUBY_SIGNATURES = ["Gemfile", "*.rb"]
PHP_SIGNATURES = ["composer.json", "*.php"]
C_SHARP_SIGNATURES = ["*.csproj", "*.sln"]

PROJECT_TYPES = [
    ("python", PYTHON_SIGNATURES),
    ("javascript", JS_SIGNATURES),
    ("java", JAVA_SIGNATURES),
    ("go", GO_SIGNATURES),
    ("rust", RUST_SIGNATURES),
    ("ruby", RUBY_SIGNATURES),
    ("php", PHP_SIGNATURES),
    ("csharp", C_SHARP_SIGNATURES),
]

CI_CD_FILES = [
    ".github/workflows",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    ".circleci/config.yml",
    ".travis.yml",
    "azure-pipelines.yml",
]

SECRET_PATTERNS = [".env", ".env.example", "secrets", "credentials", "config/secrets"]


def detect_project_type(path: str) -> str:
    base = Path(path)
    if not base.is_dir():
        return "unknown"
    for proj_type, signatures in PROJECT_TYPES:
        for sig in signatures:
            if "*" in sig:
                if list(base.glob(sig)):
                    return proj_type
            else:
                if (base / sig).exists():
                    return proj_type
    return "unknown"


def find_dependencies(path: str) -> str:
    base = Path(path)
    if not base.is_dir():
        return f"ERROR: not a directory: {base}"

    dep_files = []
    for root, _dirs, files in os.walk(base):
        for f in files:
            if f in (
                "requirements.txt", "package.json", "pyproject.toml", "Cargo.toml",
                "go.mod", "pom.xml", "build.gradle", "Gemfile", "composer.json",
                "package-lock.json", "yarn.lock", "go.sum", "Cargo.lock", "poetry.lock",
            ):
                dep_files.append(str(Path(root) / f))

    if not dep_files:
        return "(no dependency files found)"

    lines = []
    for f in dep_files:
        rel = Path(f).relative_to(base) if base in Path(f).parents else Path(f)
        content = Path(f).read_text(encoding="utf-8", errors="replace")
        lines.append(f"--- {rel} ---")
        lines.append(content)
        lines.append("")
    return "\n".join(lines)


def find_ci_cd_configs(path: str) -> list[str]:
    base = Path(path)
    if not base.is_dir():
        return []
    found = []
    for pattern in CI_CD_FILES:
        matches = list(base.glob(pattern))
        for m in matches:
            if m.is_dir():
                for f in sorted(m.rglob("*")):
                    if f.is_file():
                        found.append(str(f.relative_to(base)))
            else:
                found.append(str(m.relative_to(base)))
    return found


def find_secret_files(path: str) -> list[str]:
    base = Path(path)
    if not base.is_dir():
        return []
    found = []
    for pattern in SECRET_PATTERNS:
        matches = list(base.glob(f"**/{pattern}*"))
        for m in matches:
            if m.is_file():
                found.append(str(m.relative_to(base)))
    return found
