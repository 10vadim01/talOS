import pytest
from talos.tools.terminal import TerminalTool

@pytest.fixture
def sandbox(tmp_path):
    (tmp_path / "dummy.txt").write_text("hello")
    yield tmp_path

def test_ls(sandbox):
    term = TerminalTool(base_dir=sandbox)
    out = term.execute(command="ls")
    assert "dummy.txt" in out