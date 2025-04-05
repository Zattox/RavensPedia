from pydantic import BaseModel, EmailStr, Field


# Base model for user data.
class UserBase(BaseModel):
    email: EmailStr
    password: bytes


# Model for creating a new user.
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Password, from 5 to 50 characters",
    )


# Model for user authentication, with email and password.
class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Password, from 5 to 50 characters",
    )


# Model for the request to change a user's role.
class ChangeUserRoleRequest(BaseModel):
    user_email: str
    new_role: str


# Main user model, including the ID.
class User(UserBase):
    id: int  # User id in the database.

    class Config:
        from_attributes = True  # Enables compatibility with ORM models.


# Model for the output of authentication endpoints.
class AuthOutput(BaseModel):
    access_token: str
    refresh_token: str
