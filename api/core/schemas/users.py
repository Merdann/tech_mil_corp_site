from pydantic import BaseModel
from pydantic import Field
from pydantic import UUID4


class UserBaseForUpdatePassword(BaseModel):
    old_password: str = Field(
        min_length=8,
        max_length=20,
    )
    password: str = Field(
        min_length=8,
        max_length=20,
    )
    password_confirm: str = Field(
        min_length=8,
        max_length=20,
    )


class UserBaseForUpdate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )
    is_active: bool = False


class UserDisplayShort(BaseModel):
    username: str
    avatar: str = None

    class Config:
        orm_mode = True


class UserDisplayList(BaseModel):
    id: UUID4
    username: str
    avatar: str = None

    class Config:
        orm_mode = True


class UserDisplay(UserDisplayList):
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
