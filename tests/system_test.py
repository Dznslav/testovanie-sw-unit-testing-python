import pytest
from app import cli

@pytest.fixture
def mock_db_and_input(monkeypatch):
    monkeypatch.setattr("app.cli.DB_URL", "sqlite:///:memory:")

def test_component_full_app_lifecycle(monkeypatch, capsys):
    inputs = [
        "1", "Alice", "alice@example.com",
        "2",
        "3", "1", "Alice Smith", "alice.smith@example.com",
        "4", "1",
        "5"
    ]
    
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    
    cli.main()
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Created: Student(id=1, name='Alice', email='alice@example.com')" in output
    assert "Student(id=1, name='Alice', email='alice@example.com')" in output
    assert "Updated: Student(id=1, name='Alice Smith', email='alice.smith@example.com')" in output
    assert "Deleted." in output
    assert "Bye." in output
