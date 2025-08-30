from app.models import User

def test_password_hashing(user):
    assert user.check_password("password") is True
    assert user.check_password("wrong") is False

def test_user_email(user):
    assert user.email == "test@example.com"
