from core.schemas.users import UserDisplayShort
from pydantic import BaseModel
from pydantic import UUID4


class MainVideoDisplay(BaseModel):
    id: UUID4
    video: str

    class Config:
        orm_mode = True


class MainVideoDisplayAdmin(MainVideoDisplay):
    is_active: bool
    user: UserDisplayShort

    class Config:
        orm_mode = True
