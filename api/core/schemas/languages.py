from core.schemas.users import UserDisplayShort
from pydantic import BaseModel
from pydantic import Field
from pydantic import UUID4


class LanguageBaseForUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    is_active: bool


class LanguageBase(LanguageBaseForUpdate):
    code: str = Field(min_length=2, max_length=3)


class LanguageDisplay(BaseModel):
    name: str
    code: str

    class Config:
        orm_mode = True


class LanguageListDisplay(BaseModel):
    id: UUID4
    name: str
    code: str

    class Config:
        orm_mode = True


class LanguageDetailDisplay(LanguageBase):
    id: UUID4
    user: UserDisplayShort

    class Config:
        orm_mode = True
