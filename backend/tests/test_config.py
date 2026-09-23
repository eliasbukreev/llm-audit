from app.config import settings


def test_settings_defaults():
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000
    assert settings.llm_model == "openai/deepseek-r1:free"
    assert settings.openrouter_api_url == "https://openrouter.ai/api/v1/chat/completions"


def test_settings_paths():
    from pathlib import Path

    assert isinstance(settings.docs_dir, Path)
    assert isinstance(settings.results_dir, Path)
    assert isinstance(settings.repos_dir, Path)
    assert isinstance(settings.db_path, (Path, str))
    assert settings.docs_dir.exists()
    assert settings.results_dir.exists()


def test_settings_env_override(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "test/model")
    from app.config import Settings

    s = Settings()
    assert s.llm_model == "test/model"
