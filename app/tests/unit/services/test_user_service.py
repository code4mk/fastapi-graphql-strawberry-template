import pytest
from uuid import UUID
from app.services.user_service import UserService
from app.graphql.users.user_dto import UserRegisterDTO, UserLoginDTO, UserUpdateDTO, UserDeleteDTO
from app.models.user import User
from fastapi_pundra.gql_berry.exception import NotFoundError, DuplicateError
from fastapi import BackgroundTasks

class TestUserService:
    @pytest.mark.asyncio
    async def test_user_registration_success(self, db_session):
        """Test successful user registration."""
        class MockInfo:
            context = {
                "request": type("Request", (), {"base_url": "http://test.com/"}),
                "background_tasks": BackgroundTasks()
            }
        
        data = UserRegisterDTO(
            email="new@example.com",
            password="password1234",
            first_name="New",
            last_name="User"
        )
        
        result = await UserService.s_user_registration(MockInfo(), db_session, data)
        assert result.message == "User registered successfully"
        assert result.user.email == "new@example.com"
        
    def test_user_login_success(self, db_session):
        class MockInfo:
            context = {"request": None}
        
        data = UserLoginDTO(
            email="new@example.com",
            password="password1234"
        )
        
        result = UserService.s_user_login(MockInfo(), db_session, data)
        assert result.user.email == "new@example.com"
        assert result.token_type == "Bearer"
        
    def test_get_users_list(self, db_session):
        class MockInfo:
            context = {"request": None}
            
        result = UserService.s_users(MockInfo(), db_session, page=1, per_page=10)
        assert len(result.data) > 0
        assert result.pagination["total"] > 0
        
    def test_update_user(self, db_session):
        class MockInfo:
            context = {"request": None}
        
        user = db_session.query(User).first()
        data = UserUpdateDTO(
            id=user.id,
            first_name="Updated",
            last_name="Name"
        )
        
        result = UserService.s_user_update(MockInfo(), db_session, data)
        assert result.user.first_name == "Updated"
        assert result.user.last_name == "Name"
        
    def test_delete_user(self, db_session):
        class MockInfo:
            context = {"request": None}
        
        user = db_session.query(User).first()
        data = UserDeleteDTO(user_id=user.id)
        
        result = UserService.s_user_delete(MockInfo(), db_session, data)
        assert result.message == "User deleted successfully"

    @pytest.mark.asyncio
    async def test_user_registration_duplicate_email(self, db_session):
        """Test user registration with duplicate email."""
        class MockInfo:
            context = {
                "request": type("Request", (), {"base_url": "http://test.com/"}),
                "background_tasks": BackgroundTasks()
            }
        
        # First registration
        data = UserRegisterDTO(
            email="duplicate@example.com",
            password="password1234",
            first_name="First",
            last_name="User"
        )
        await UserService.s_user_registration(MockInfo(), db_session, data)
        
        # Second registration with same email
        with pytest.raises(DuplicateError) as exc_info:
            await UserService.s_user_registration(MockInfo(), db_session, data)
        assert str(exc_info.value) == "User with email duplicate@example.com already exists"

    def test_user_login_invalid_credentials(self, db_session):
        """Test user login with invalid credentials."""
        class MockInfo:
            context = {"request": None}
        
        # Test with non-existent email
        data = UserLoginDTO(
            email="nonexistent@example.com",
            password="password1234"
        )
        with pytest.raises(NotFoundError) as exc_info:
            UserService.s_user_login(MockInfo(), db_session, data)
        assert str(exc_info.value) == "Your email or password is incorrect"
        
        # Test with wrong password
        data = UserLoginDTO(
            email="new@example.com",  # existing email from previous test
            password="wrongpassword"
        )
        with pytest.raises(NotFoundError) as exc_info:
            UserService.s_user_login(MockInfo(), db_session, data)
        assert str(exc_info.value) == "Your email or password is incorrect"

    def test_update_user_not_found(self, db_session):
        """Test updating non-existent user."""
        class MockInfo:
            context = {"request": None}
        
        data = UserUpdateDTO(
            id=UUID('00000000-0000-0000-0000-000000000000'),
            first_name="Updated"
        )
        
        with pytest.raises(NotFoundError) as exc_info:
            UserService.s_user_update(MockInfo(), db_session, data)
        assert str(exc_info.value) == "User with id 00000000-0000-0000-0000-000000000000 not found"

    def test_delete_user_not_found(self, db_session):
        """Test deleting non-existent user."""
        class MockInfo:
            context = {"request": None}
        
        data = UserDeleteDTO(user_id=UUID('00000000-0000-0000-0000-000000000000'))
        
        with pytest.raises(NotFoundError) as exc_info:
            UserService.s_user_delete(MockInfo(), db_session, data)
        assert str(exc_info.value) == "User with id 00000000-0000-0000-0000-000000000000 not found" 