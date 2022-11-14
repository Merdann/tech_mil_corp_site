from pydantic import BaseModel
from pydantic import Field


class AccessRefreshTokenDisplay(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)


class AccessTokenForGetRefreshTokenBase(BaseModel):
    access_token: str = Field(...)


class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )
    password: str = Field(
        min_length=8,
        max_length=20,
    )


class UserBaseSignUp(UserBase):
    password_confirm: str = Field(
        min_length=8,
        max_length=20,
    )
