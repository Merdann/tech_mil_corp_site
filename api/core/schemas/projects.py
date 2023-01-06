from typing import List

from core.schemas.languages import LanguageListDisplay
from core.schemas.users import UserDisplayShort
from pydantic import BaseModel
from pydantic import UUID4


class ProjectImageDisplay(BaseModel):
    id: UUID4
    image: str

    class Config:
        orm_mode = True


class ProjectVideoDisplay(BaseModel):
    id: UUID4
    video: str

    class Config:
        orm_mode = True


class ProjectDisplay(BaseModel):
    id: UUID4
    multimedia: str

    class Config:
        orm_mode = True


class ProjectListDisplay(BaseModel):
    id: UUID4
    title_highlight: str
    multimedia: str

    class Config:
        orm_mode = True


class ProjectDetailDisplay(BaseModel):
    id: UUID4
    multimedia: str
    project_images: List[ProjectImageDisplay] = []
    project_videos: List[ProjectVideoDisplay] = []

    class Config:
        orm_mode = True


class ProjectTranslationListDisplay(BaseModel):
    title_highlight: str
    project: ProjectDisplay

    class Config:
        orm_mode = True


class ProjectTranslationDetailDisplay(BaseModel):
    title_highlight: str
    description: str
    project: ProjectDetailDisplay

    class Config:
        orm_mode = True


class ProjectTranslationDetailDisplayAdmin(ProjectTranslationDetailDisplay):
    is_active: bool
    language: LanguageListDisplay
    user: UserDisplayShort

    class Config:
        orm_mode = True
