from core.schemas.users import UserDisplayShort
from pydantic import BaseModel
from pydantic import UUID4


class CarouselAboutDisplayClient(BaseModel):
    image: str

    class Config:
        orm_mode = True


class CarouselAboutDisplay(CarouselAboutDisplayClient):
    id: UUID4

    class Config:
        orm_mode = True


class CarouselAboutDetailDisplayAdmin(CarouselAboutDisplay):
    is_active: bool
    user: UserDisplayShort

    class Config:
        orm_mode = True
