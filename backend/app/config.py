import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/deepseek-r1:free")

DOCS_DIR = os.environ.get("DOCS_DIR", os.path.join(BASE_DIR, "..", "docs"))
RESULTS_DIR = os.environ.get("RESULTS_DIR", os.path.join(BASE_DIR, "..", "results"))
REPOS_DIR = os.environ.get("REPOS_DIR", os.path.join(BASE_DIR, "..", "repos-for-analysis"))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "audit.db"))
