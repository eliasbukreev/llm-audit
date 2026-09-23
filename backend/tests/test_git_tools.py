from app.config import settings
from app.tools import git_tools


def test_git_clone_invalid():
    result = git_tools.git_clone("https://github.com/nonexistent/repo-12345")
    assert "ERROR" in result


def test_get_structure_nonexistent():
    result = git_tools.get_structure("/nonexistent/path")
    assert "ERROR" in result


def test_get_structure_valid():
    result = git_tools.get_structure(str(settings.repos_dir))
    assert "📁" in result


def test_get_history_nonexistent():
    result = git_tools.get_history("/nonexistent/path")
    assert isinstance(result, list)
    assert len(result) == 1
    assert "error" in result[0]


def test_get_history_valid():
    result = git_tools.get_history(str(settings.repos_dir))
    assert isinstance(result, list)
