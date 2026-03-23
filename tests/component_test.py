import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.repository import StudentRepository
from app.service import StudentService

@pytest.fixture(scope="function")
def service_component():

    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = Session()
    
    repo = StudentRepository(session)
    service = StudentService(repo)
    
    yield service
    
    session.close()
    Base.metadata.drop_all(engine)

def test_component_service_create_and_list_lifecycle(service_component):

    service_component.create_student("Alice Cooper", "alice@example.com")
    service_component.create_student("Bob Builder", "bob@example.com")
    
    students = service_component.list_students()
    
    assert len(students) == 2
    assert any(s.name == "Alice Cooper" for s in students)
    assert any(s.email == "bob@example.com" for s in students)

def test_component_service_business_validations(service_component):

    with pytest.raises(ValueError, match="Name must have at least 2 characters."):
        service_component.create_student("A", "a@example.com")
    
    with pytest.raises(ValueError, match="Invalid email address."):
        service_component.create_student("John", "bad-email")

def test_component_service_delete_flow(service_component):

    student = service_component.create_student("To Be Deleted", "delete@example.com")
    
    service_component.delete_student(student.id)
    
    students = service_component.list_students()
    assert len(students) == 0
    
    with pytest.raises(ValueError, match="Student not found."):
        service_component.delete_student(student.id)
