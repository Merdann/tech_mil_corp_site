import ujson
from core.schemas.languages import LanguageDisplay
from core.schemas.users import UserDisplayShort
from pydantic import BaseModel
from pydantic import Field
from pydantic import UUID4


class CarouselMainDisplayClient(BaseModel):
    image: str

    class Config:
        orm_mode = True


class CarouselMainDisplay(CarouselMainDisplayClient):
    id: UUID4

    class Config:
        orm_mode = True


class CarouselMainDetailDisplayAdmin(CarouselMainDisplay):
    is_active: bool
    user: UserDisplayShort

    class Config:
        orm_mode = True
