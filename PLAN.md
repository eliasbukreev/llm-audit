# План реализации: Desktop-приложение для аудита репозиториев по ГОСТ Р 56939-2024

## Цель

Превратить шаблон workflow для KiloCode в полноценное десктоп-приложение: пользователь вставляет URL репозитория → приложение клонирует его, запускает многошаговый AI-анализ по ГОСТ Р 56939-2024 и выдаёт результаты (Markdown + DOCX).

---

## Архитектура

```
┌──────────────┐   HTTP localhost:8000   ┌──────────────────────┐
│  Tauri App   │ ◄──────────────────────► │  FastAPI Backend     │
│  Vue 3 + TS  │   SSE для прогресса     │  (Python)            │
│  ~50 строк   │                         │  LangGraph + Tools   │
│  Rust shell  │                         │                      │
└──────────────┘                         └──────────┬───────────┘
                                                        │
                                               ┌────────▼────────┐
                                               │  OpenRouter     │
                                               │  (Free Models)  │
                                               └─────────────────┘
```

- **Tauri** — десктоп-обёртка (Rust shell + Vue 3 UI), лёгкий (~10 MB)
- **FastAPI** — HTTP API + SSE для прогресса + запуск LangGraph
- **LangGraph** — оркестрация шагов аудита (5.1 → 5.3 → 5.4 → 5.5 → 5.6)
- **SQLite** — персистентность сессий, шагов, результатов
- **OpenRouter** — доступ к бесплатным LLM через OpenAI-совместимый API
- **pandoc** — конвертация Markdown → DOCX

---

## Решения

| Решение | Выбор |
|---------|-------|
| Бэкенд | FastAPI (async, Python 3.12+) |
| Оркестрация LLM | LangGraph (nodes + edges, рёбра задают порядок по ГОСТ) |
| LLM-провайдер | OpenRouter (openai/deepseek-r1:free или аналог) |
| UI | Vue 3 + Vite + TypeScript |
| Десктоп-обёртка | Tauri (минимальный Rust, весь UI на Vue) |
| БД | SQLite (sqlite-utils) |
| Package manager (Python) | uv (pyproject.toml + uv.lock) |
| Package manager (Node) | pnpm |
| Контейнеризация | Docker Compose (backend + frontend) |
| DOCX-конвертация | pandoc CLI |
| Прогресс в реальном времени | SSE через EventBus (asyncio.Queue) |
| MVP | Шаг 5.1 (анализ текущего состояния) |

---

## Структура проекта

```
llm-server-dib/
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # OPENROUTER_API_KEY, LLM_MODEL, HOST, PORT
│   │   ├── database.py          # SQLite init + session CRUD
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── audit.py         # AuditSession, AuditStep (Pydantic)
│   │   │   └── repo.py          # RepoInfo
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── audit.py         # POST /audit/start, GET /audit/{id}/stream (SSE),
│   │   │   │                      # GET /audit/{id}/results, GET /audit/{id}/download/{file}
│   │   │   └── health.py        # GET /health
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   └── state_graph.py   # LangGraph: START→5.1→END (MVP);
│   │   │                          # рёбра для 5.3–5.6 закомментированы
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── step_51.py       # Agent: анализ текущего состояния (MVP)
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── filesystem.py    # read_file, list_dir, search_files
│   │   │   ├── git_tools.py     # git_clone, get_structure, get_history
│   │   │   ├── project_tools.py # detect_project_type, find_dependencies,
│   │   │   │                      # find_ci_cd_configs, find_secret_files
│   │   │   └── doc_tools.py     # write_result, get_plan, convert_to_docx
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── llm.py           # OpenRouter client (OpenAI SDK), build_messages
│   │       ├── storage.py       # Path resolution: docs/, results/, repos-for-analysis/
│   │       └── pandoc.py        # pandoc CLI wrapper
│   ├── db/
│   │   └── schema.sql           # sessions, steps, files tables
│   ├── pyproject.toml           # Зависимости (uv)
│   ├── uv.lock                  # Lock-файл (uv)
│   ├── Dockerfile               # Python + uv + pandoc + git
│   └── .env.example
│
├── frontend/                     # Tauri + Vue 3
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx              # Состояние: Idle → Cloning → Analysing → Done / Error
│   │   ├── components/
│   │   │   ├── UrlInput.tsx      # Поле ввода URL + кнопка «Начать аудит»
│   │   │   ├── ProgressPanel.tsx # Карточки шагов (статус, логи)
│   │   │   ├── ResultViewer.tsx  # Просмотр Markdown результата
│   │   │   └── DownloadPanel.tsx # Кнопки: .md, .docx
│   │   ├── hooks/
│   │   │   ├── useAudit.ts       # POST /audit/start, SSE /audit/{id}/stream
│   │   │   └── useSSE.ts         # SSE клиент
│   │   ├── lib/
│   │   │   └── api.ts            # HTTP клиент к FastAPI
│   │   └── types/
│   │       └── audit.ts          # TypeScript типы (mirror shared/types.ts)
│   ├── src-tauri/
│   │   ├── Cargo.toml
│   │   ├── tauri.conf.json
│   │   ├── src/
│   │   │   └── main.rs           # ~50 строк: spawn server, menu, file dialog
│   │   └── icons/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── vite-env.d.ts
│   └── Dockerfile               # Node + pnpm + Tauri build
│
├── shared/
│   └── types.ts                  # AuditSession, AuditStep, StepStatus (TS)
│
├── docs/                         # Без изменений (из исходного проекта)
│   ├── plans/                    # 5 планов (инструкции для агентов)
│   ├── templates/                # 5 шаблонов-примеров (ОПРОСНИК)
│   └── standarts/ГОСТ Р 56939— 2024.md
│
├── workflows/                    # Без изменений
│   └── create-security-audit.md
│
├── results/                      # Результаты аудита (git-ignored)
├── .gitignore
├── .env                          # Не коммитить
├── docker-compose.yml            # Backend + Frontend
├── PLAN.md                       # Этот файл
└── README.md
```

---

## Ключевые механизмы

### Запуск задачи

```
POST /audit/start {url: "..."}
  ├── SQLite: INSERT session (status=running) + steps (5.1=pending)
  ├── EventBus: создаёт asyncio.Queue для session_id
  ├── asyncio.create_task(run_audit(session_id, url))
  └── Returns {session_id}
```

### Прогресс через EventBus + SSE

```python
event_bus: dict[str, asyncio.Queue] = {}

async def run_audit(session_id, url):
    event_bus[session_id].put({"step": "setup", "status": "running", "log": "Cloning..."})
    git_clone(url, repo_path)
    event_bus[session_id].put({"step": "setup", "status": "done"})

    event_bus[session_id].put({"step": "5.1", "status": "running"})
    result = await graph.ainvoke({"session_id": session_id})
    event_bus[session_id].put({"step": "5.1", "status": "done", "result_path": result.path})

    event_bus[session_id].put({"step": "complete", "status": "done"})
```

```python
@router.get("/audit/{session_id}/stream")
async def stream(session_id: str):
    queue = event_bus[session_id]
    async def generator():
        while True:
            event = await queue.get()
            yield f"data: {json.dumps(event)}\n\n"
            if event.get("step") == "complete":
                break
    return StreamingResponse(generator(), media_type="text/event-stream")
```

### LangGraph (MVP)

```
START → Node 5.1 → END
```

Будущие рёбра (закомментированы): `5.1 → 5.3, 5.1 → 5.4, 5.1 → 5.5, {5.3,5.4,5.5} → 5.6 → END`

### Tools внутри агентов

| Шаг | Доступные tools |
|-----|----------------|
| 5.1 | read_file, list_dir, search_files, detect_project_type, find_dependencies, find_ci_cd_configs, find_secret_files, get_plan("5.1"), write_result |
| 5.3 | read_file, read_result("5.1"), get_plan("5.3"), write_result |
| 5.4 | read_file, read_result("5.1"), get_plan("5.4"), write_result |
| 5.5 | read_file, read_result("5.1"), get_plan("5.5"), write_result |
| 5.6 | read_file, read_result("5.1"), read_result("5.3"), get_plan("5.6"), write_result |

---

## Порядок реализации

| Этап | Содержание | Коммит |
|------|------------|--------|
| 1 | Структура: `pyproject.toml`, `uv.lock`, `package.json`, `shared/types.ts`, `.gitignore`, `README.md` | 1 |
| 2 | Backend core: `config.py`, `database.py`, `models/`, `db/schema.sql`, `api/health.py`, `main.py` | 2 |
| 3 | Tools: `filesystem.py`, `git_tools.py`, `project_tools.py`, `doc_tools.py`, `services/llm.py`, `services/storage.py`, `services/pandoc.py` | 3 |
| 4 | Agent 5.1 + LangGraph: `agents/step_51.py`, `graph/state_graph.py`, `api/audit.py` | 4 |
| 5 | Frontend Tauri init + Vue scaffold: `src/main.tsx`, `App.tsx`, базовые компоненты | 5 |
| 6 | Frontend логика: хуки (`useAudit`, `useSSE`), `lib/api.ts`, типы, компоненты | 6 |
| 7 | Tauri shell: `src/main.rs` (spawn server, menu, dialogs) | 7 |
| 8 | Docker: `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml` | 8 |
| 9 | Integration + polish: DOCX export, error handling, final UX | 9 |

---

## Workflow команд разработки

```bash
# Первый раз (локально без Docker)
cd backend && uv sync
cd frontend && corepack enable && pnpm install

# Разработка в контейнере
docker compose up --build
docker compose exec backend bash   # uvicorn app.main:app --reload
docker compose exec frontend bash  # pnpm dev / pnpm tauri dev

# Запуск бэкенда локально
cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Зависимости (backend)

- fastapi, uvicorn[standard]
- langgraph, langchain-openai, openai
- pydantic, httpx
- sqlite-utils
- python-dotenv
- structlog

## Зависимости (frontend)

- vue (3.x)
- @tauri-apps/api
- pnpm

---

## Дефолтные значения (.env.example)

```env
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL=openai/deepseek-r1:free
HOST=0.0.0.0
PORT=8000
```
