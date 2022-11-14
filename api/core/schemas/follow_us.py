from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import UUID4


class FollowUsBase(BaseModel):
    email: EmailStr


class FollowUsDisplay(FollowUsBase):
    id: UUID4

    class Config:
        orm_mode = True
