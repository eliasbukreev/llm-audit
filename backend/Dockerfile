FROM python:3.12-slim

RUN apt-get update && apt-get install -y git pandoc && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock* /app/
COPY backend/app/ /app/app/
COPY backend/db/ /app/db/

RUN uv pip install --system --no-dev .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
