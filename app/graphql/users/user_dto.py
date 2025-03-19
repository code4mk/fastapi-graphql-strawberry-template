from pydantic import BaseModel, EmailStr
from pydantic import field_validator, Field
from uuid import UUID


class UserRegisterDTO(BaseModel):
    email: EmailStr = Field(..., description="User's email address (required)")
    password: str = Field(..., description="Password must be at least 8 characters long (required)")
    first_name: str | None = Field(None, description="User's first name (optional)")
    last_name: str | None = Field(None, description="User's last name (optional)")

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate the password."""
        if len(v) < 8:
            error_message = "Password must be at least 8 characters long"
            raise ValueError(error_message)
        return v


class UserLoginDTO(BaseModel):
    email: EmailStr = Field(..., description="User's email address (required)")
    password: str = Field(..., description="User's password (required)")


class UserUpdateDTO(BaseModel):
    id: UUID = Field(..., description="User's id (required)")
    first_name: str | None = Field(None, description="User's first name (optional)")
    last_name: str | None = Field(None, description="User's last name (optional)")
    is_active: bool | None = Field(
        None, description="Whether the user account is active (optional)"
    )


class UserDeleteDTO(BaseModel):
    user_id: UUID = Field(..., description="User's id (required)")
