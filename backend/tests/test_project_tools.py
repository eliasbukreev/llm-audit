from app.config import BASE_DIR
from app.tools import project_tools


def test_detect_project_type_backend():
    result = project_tools.detect_project_type(str(BASE_DIR))
    assert result in ("unknown", "python")


def test_detect_project_type_nonexistent():
    result = project_tools.detect_project_type("/nonexistent")
    assert result == "unknown"


def test_find_dependencies_backend():
    result = project_tools.find_dependencies(str(BASE_DIR.parent))
    assert "pyproject.toml" in result


def test_find_dependencies_root():
    result = project_tools.find_dependencies(str(BASE_DIR))
    assert "pyproject.toml" not in result
    assert "requirements.txt" not in result


def test_find_dependencies_nonexistent():
    result = project_tools.find_dependencies("/nonexistent")
    assert "ERROR" in result


def test_find_ci_cd_configs_backend():
    result = project_tools.find_ci_cd_configs(str(BASE_DIR))
    assert isinstance(result, list)


def test_find_ci_cd_configs_nonexistent():
    result = project_tools.find_ci_cd_configs("/nonexistent")
    assert result == []


def test_find_secret_files_backend():
    result = project_tools.find_secret_files(str(BASE_DIR))
    assert isinstance(result, list)


def test_find_secret_files_nonexistent():
    result = project_tools.find_secret_files("/nonexistent")
    assert result == []
