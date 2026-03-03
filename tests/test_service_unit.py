import pytest
from unittest.mock import Mock
from app.service import StudentService

def test_create_student_success():
    repo = Mock()
    repo.create.return_value = {
        "id": 1,
        "name": "Dominik",
        "email": "dominik@example.com"
    }

    service = StudentService(repo)
    result = service.create_student("Dominik", "DOMINIK@example.com")

    repo.create.assert_called_once_with("Dominik", "dominik@example.com")
    assert result["email"] == "dominik@example.com"

def test_create_student_invalid_name():
    repo = Mock()
    service = StudentService(repo)

    with pytest.raises(ValueError, match="Name must have at least 2 characters."):
        service.create_student("A", "a@example.com")

def test_create_student_invalid_email():
    repo = Mock()
    service = StudentService(repo)

    with pytest.raises(ValueError, match="Invalid email address."):
        service.create_student("Dominik", "zly_email")

def test_update_student_not_found():
    repo = Mock()
    repo.update.return_value = None
    service = StudentService(repo)

    with pytest.raises(ValueError, match="Student not found."):
        service.update_student(1, "New Name", "new@example.com")

def test_delete_student_invalid_id():
    repo = Mock()
    service = StudentService(repo)

    with pytest.raises(ValueError, match="student_id must be > 0"):
        service.delete_student(0)

def test_list_students_returns_one_student():
    repo = Mock()
    repo.get_all.return_value = [
        {"id": 1, "name": "Dominik", "email": "dominik@example.com"}
    ]

    service = StudentService(repo)

    students = service.list_students()

    repo.get_all.assert_called_once()
    assert len(students) == 1
    assert students[0]["name"] == "Dominik"
    assert students[0]["email"] == "dominik@example.com"
