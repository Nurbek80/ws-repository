import pytest
from main import User, UserService
from repos.in_memory import InMemoryRepository

@pytest.fixture
def user_service():
    repo = InMemoryRepository()
    return UserService(repo)

def test_register_and_find_user(user_service):
    user = User(name="Test User", email="test@example.com", age=25)
    user_service.register(user)
    fetched_user = user_service.find_by_email("test@example.com")
    
    assert fetched_user.name == "Test User"
    assert fetched_user.email == "test@example.com"
    assert fetched_user.age == 25

def test_duplicate_email_raises_error(user_service):
    user = User(name="Test User", email="test@example.com", age=25)
    user_service.register(user)
    
    with pytest.raises(ValueError, match="duplicate email"):
        user_service.register(user)

def test_find_non_existent_user_returns_none(user_service):
    fetched_user = user_service.find_by_email("nobody@example.com")
    assert fetched_user is None