from pydantic import BaseModel, EmailStr, Field


# The base class for the User (without id)
class UserBase(BaseModel):
    email: EmailStr
    password: bytes


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Password, from 5 to 50 characters",
    )


class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Password, from 5 to 50 characters",
    )

class ChangeUserRoleRequest(BaseModel):
    user_email: str
    new_role: str

# The main class for work with a User
class User(UserBase):
    id: int  # User id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models


class AuthOutput(BaseModel):
    access_token: str
    refresh_token: str
