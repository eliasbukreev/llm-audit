# llm-server-dib

Desktop-приложение для аудита репозиториев по ГОСТ Р 56939-2024 (разработка безопасного ПО).

## Архитектура

- **Frontend**: Tauri + Vue 3 + TypeScript
- **Backend**: FastAPI (Python) + LangGraph
- **LLM**: OpenRouter (Free Models)
- **Database**: SQLite
- **Package managers**: uv (Python), pnpm (Node)
- **Dev env**: Docker Compose

## Быстрый старт (Docker)

```bash
docker compose up --build
```

## Локальная разработка

### Backend
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
corepack enable && pnpm install
pnpm dev  # или pnpm tauri dev для десктоп-окна
```

## Структура

```
backend/          FastAPI + LangGraph + Tools
frontend/         Tauri + Vue 3
shared/           Общие типы (TS)
docs/             Планы, шаблоны, ГОСТ
workflows/        Workflow-инструкции
results/          Результаты аудита (git-ignored)
```

## Смотрите также

- [PLAN.md](./PLAN.md) — детальный план реализации
