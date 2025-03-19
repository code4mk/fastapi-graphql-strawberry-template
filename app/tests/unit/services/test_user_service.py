import pytest
from uuid import UUID
from app.services.user_service import UserService
from app.graphql.users.user_dto import UserRegisterDTO, UserLoginDTO, UserUpdateDTO
from app.models.user import User
from fastapi_pundra.gql_berry.exception import NotFoundError, DuplicateError
from fastapi import BackgroundTasks

class TestUserService:
    async def test_user_registration_success(self, db_session):
        # Create mock info and data
        class MockInfo:
            context = {
                "request": type("Request", (), {"base_url": "http://test.com/"}),
                "background_tasks": BackgroundTasks()
            }
        
        data = UserRegisterDTO(
            email="new3@example.com",
            password="password123",
            first_name="New",
            last_name="User"
        )
        
        # Execute registration
        result = await UserService.s_user_registration(MockInfo(), data)
        
        # Assertions
        assert result.message == "User registered successfully"
        assert result.user.email == "new3@example.com"
        assert result.user.first_name == "New"
        assert result.user.last_name == "User"
        
    async def test_user_registration_duplicate_email(self, db_session):
        class MockInfo:
            context = {
                "request": type("Request", (), {"base_url": "http://test.com/"}),
                "background_tasks": BackgroundTasks()
            }
        
        data = UserRegisterDTO(
            email="new3@example.com",
            password="password123",
            first_name="New",
            last_name="User"
        )
        
        with pytest.raises(DuplicateError) as exc_info:
            await UserService.s_user_registration(MockInfo(), data)
        
        assert f"User with email new3@example.com already exists" in str(exc_info.value)

    def test_user_login_success(self, db_session):
        class MockInfo:
            context = {"request": None}
        
        data = UserLoginDTO(
            email="new3@example.com",
            password="password123"
        )
        
        result = UserService.s_user_login(MockInfo(), data)
        
        assert result.user.email == "new3@example.com"
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "Bearer"

    def test_user_login_invalid_credentials(self, db_session):
        class MockInfo:
            context = {"request": None}
        
        data = UserLoginDTO(
            email="wrong@example.com",
            password="wrongpass"
        )
        
        with pytest.raises(NotFoundError) as exc_info:
            UserService.s_user_login(MockInfo(), data)
        
        assert "Your email or password is incorrect" in str(exc_info.value) 