from app.config import settings
from app.tools import filesystem


def test_read_file_valid():
    plan_file = (
        settings.docs_dir
        / "plans"
        / "Анализ текущего состояния процессов разработки безопасного ПО.md"
    )
    content = filesystem.read_file(str(plan_file))
    assert len(content) > 0
    assert "ГОСТ" in content


def test_read_file_not_found():
    result = filesystem.read_file("/nonexistent/file.txt")
    assert "ERROR" in result


def test_read_file_outside_allowed():
    result = filesystem.read_file("/etc/passwd")
    assert "ERROR" in result
    assert "outside allowed" in result


def test_list_dir_docs():
    result = filesystem.list_dir(str(settings.docs_dir))
    assert "plans/" in result
    assert "templates/" in result


def test_list_dir_nonexistent():
    result = filesystem.list_dir("/nonexistent/dir")
    assert "ERROR" in result


def test_list_dir_outside_allowed():
    result = filesystem.list_dir("/etc")
    assert "ERROR" in result
    assert "outside allowed" in result


def test_search_files_valid():
    results = filesystem.search_files(str(settings.docs_dir), "*.md")
    assert len(results) >= 1


def test_search_files_outside():
    results = filesystem.search_files("/etc", "*.conf")
    assert len(results) == 1
    assert "ERROR" in results[0]
