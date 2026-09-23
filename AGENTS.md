# AGENTS.md

## Проект

Десктопное приложение для аудита репозиториев по ГОСТ Р 56939-2024 (безопасная разработка ПО).

## Архитектура

- **Frontend**: Tauri + Vue 3 + TypeScript + NaiveUI (`frontend/`)
- **Backend**: FastAPI + Python (`backend/`)
- **LLM**: OpenRouter (https://openrouter.ai/api/v1/chat/completions)
- **БД**: SQLite (raw sqlite3, без ORM)
- **Оркестрация**: LangGraph (пока skeleton)

## Структура

```
backend/
  app/
    config.py        — Settings (pydantic-settings), BASE_DIR = app/
    main.py          — FastAPI app
    database.py      — SQLite init
    models/          — Pydantic models (audit, repo)
    api/             — FastAPI routers (health, audit)
    tools/           — Agent tools (filesystem, git_tools, project_tools, doc_tools)
    agents/          — LangChain agents (planned)
    graph/           — LangGraph state machine (planned)
    services/        — LLM client (planned)
  tests/             — pytest tests
  pyproject.toml     — deps + ruff/mypy/pytest config
  uv.lock
frontend/
  src/               — Vue 3 components
frontend/
  package.json
  vite.config.ts
  tsconfig.json
docs/                — Plans, templates, reports
results/             — Analysis output
repos-for-analysis/  — Cloned repos
PLAN.md              — Implementation plan
```

## Ключевые детали

- `BASE_DIR` в config.py — это `backend/app/` (module-level, не поле Settings)
- Пути в Settings: `docs_dir = BASE_DIR.parent.parent / "docs"` (= project root/docs/)
- `ALLOWED_ROOTS` в filesystem.py включает: repos_dir, docs_dir, results_dir, BASE_DIR
- Temp-пути (/tmp) НЕ в ALLOWED_ROOTS — read_file/write_result/validate их отвергают
- `find_dependencies` ищет только в корне переданного path (не рекурсивно)
- Pyproject.toml находится в `backend/`, НЕ в project root

## Команды проверки

### Backend (cd backend/)
```bash
uv run ruff check .           # Lint
uv run ruff check . --fix     # Auto-fix
uv run mypy app/              # Type check (lenient)
uv run pytest tests/ -v       # Tests
uv run python -m app.main     # Сервер
```

### Frontend (cd frontend/)
```bash
./node_modules/.bin/eslint .       # Lint
./node_modules/.bin/vue-tsc --noEmit  # Type check
./node_modules/.bin/prettier --check .  # Format
```

### Полная проверка (обе директории)
```bash
cd backend && uv run ruff check . && uv run mypy app/ && uv run pytest tests/ -v
cd frontend && ./node_modules/.bin/eslint . && ./node_modules/.bin/vue-tsc --noEmit && ./node_modules/.bin/prettier --check .
```

## Установка

### Backend
```bash
cd backend
uv sync
uv run python -m app.main
```

### Frontend
```bash
cd frontend
pnpm install
pnpm run tauri dev
```

## Напоминания

- НЕ коммитить без явного запроса пользователя
- Делать инкрементальные шаги, показывать результат после каждого
- Plan.md — главный ориентир для реализации
