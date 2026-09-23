from app.config import settings as s
from app.tools import doc_tools


def test_get_plan_valid():
    result = doc_tools.get_plan("5.1")
    assert len(result) > 0
    assert "ГОСТ" in result


def test_get_plan_invalid():
    result = doc_tools.get_plan("9.9")
    assert "ERROR" in result
    assert "unknown step" in result


def test_write_result():
    test_path = s.results_dir / "test-write.md"
    try:
        result = doc_tools.write_result(str(test_path), "# Hello")
        assert "OK" in result
        assert test_path.exists()
        assert test_path.read_text() == "# Hello"
    finally:
        if test_path.exists():
            test_path.unlink()


def test_write_result_nested_dir():
    test_path = s.results_dir / "nested" / "deep" / "write.md"
    try:
        result = doc_tools.write_result(str(test_path), "# Deep")
        assert "OK" in result
        assert test_path.exists()
    finally:
        import shutil
        if test_path.parent.exists():
            shutil.rmtree(test_path.parent)


def test_convert_to_docx():
    test_input = s.results_dir / "test-input.md"
    test_output = s.results_dir / "test-output.docx"
    try:
        doc_tools.write_result(str(test_input), "# Test")
        result = doc_tools.convert_to_docx(str(test_input), str(test_output))
        if "ERROR" in result:
            assert "pandoc" in result
        else:
            assert test_output.exists()
    finally:
        for p in [test_input, test_output]:
            if p.exists():
                p.unlink()
