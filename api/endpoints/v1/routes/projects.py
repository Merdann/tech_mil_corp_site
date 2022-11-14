from typing import List
from typing import Optional
from uuid import UUID

from core.database.base.session import get_db
from core.database.repository import projects
from core.database.repository.languages import default_lang
from core.schemas.projects import ProjectListDisplay
from core.schemas.projects import ProjectTranslationDetailDisplay
from core.schemas.projects import ProjectTranslationDetailDisplayAdmin
from core.schemas.projects import ProjectTranslationListDisplay
from core.security import JWTBearer
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi import UploadFile
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.get(
    "/all",
    response_model=List[ProjectTranslationListDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_projects_client(
    lang: str = default_lang(), db: Session = Depends(get_db)
):
    all_projects = projects.get_all_projects_client(lang, db)
    return all_projects


@router.get(
    "/{project_id}",
    response_model=ProjectTranslationDetailDisplay,
    status_code=status.HTTP_200_OK,
)
async def get_one_project_client(
    project_id: UUID,
    lang: str = default_lang(),
    db: Session = Depends(get_db),
):
    project = projects.get_one_project_client(project_id, lang, db)
    return project


@router.post(
    "/admin/create",
    response_model=ProjectTranslationDetailDisplayAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_translation(
    req: Request,
    title_highlight: str = Form(min_length=1, max_length=50),
    title_head: str = Form(min_length=1, max_length=50),
    description: str = Form(min_length=1, max_length=500),
    origin_elem_id: Optional[UUID] = Form(None),
    lang_code: str = Form(min_length=2, max_length=2, default=default_lang()),
    multimedia: UploadFile = File(
        None,
        description="This field is required when you create "
        "first (english language) item",
    ),
    project_images: List[UploadFile] = File(None),
    project_videos: List[UploadFile] = File(None),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):

    project = await projects.create_project_translation(
        req,
        title_highlight,
        title_head,
        description,
        origin_elem_id,
        lang_code,
        multimedia,
        project_images,
        project_videos,
        tkn,
        db,
    )
    return project


@router.get(
    "/admin/all",
    response_model=List[ProjectListDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_projects_admin(
    tkn: str = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    all_projects = projects.get_all_projects_admin(db, tkn)
    return all_projects


@router.get(
    "/admin/{project_id}",
    response_model=ProjectTranslationDetailDisplayAdmin,
    status_code=status.HTTP_200_OK,
)
async def get_one_project_admin(
    project_id: UUID,
    lang: str = default_lang(),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    project = projects.get_one_project_admin(project_id, lang, tkn, db)
    return project


@router.put(
    "/admin/{project_id}",
    response_model=ProjectTranslationDetailDisplayAdmin,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_project_admin(
    project_id: UUID,
    req: Request,
    title_highlight: str = Form(min_length=1, max_length=50, default=None),
    title_head: str = Form(min_length=1, max_length=50, default=None),
    description: str = Form(min_length=1, max_length=500, default=None),
    lang_code: str = Form(min_length=2, max_length=2, default=default_lang()),
    multimedia: UploadFile = File(None),
    is_active: bool = Form(True),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    project = await projects.update_project_admin(
        req,
        project_id,
        title_highlight,
        title_head,
        description,
        lang_code,
        multimedia,
        is_active,
        tkn,
        db,
    )
    return project


@router.post(
    "/admin/{project_id}/add_project_images",
    response_model=ProjectTranslationDetailDisplayAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def add_project_images_admin(
    project_id: UUID,
    req: Request,
    default_language: str = Form(default=default_lang()),
    project_images: List[UploadFile] = File(None),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    project = projects.add_project_images_admin(
        req,
        project_id,
        default_language,
        project_images,
        tkn,
        db,
    )
    return project


@router.put(
    "/admin/{project_id}/update_project_image/{project_image_id}",
    response_model=ProjectTranslationDetailDisplayAdmin,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_project_image_admin(
    req: Request,
    project_id: UUID,
    project_image_id: UUID,
    new_project_image: UploadFile = File(...),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    project = projects.update_project_image_admin(
        req,
        project_id,
        project_image_id,
        new_project_image,
        tkn,
        db,
    )
    return project


@router.delete(
    "/admin/{project_id}/delete_project_image/{project_image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project_image_admin(
    project_id: UUID,
    project_image_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    projects.delete_project_image_admin(
        project_id,
        project_image_id,
        tkn,
        db,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/admin/{project_id}/add_project_videos",
    response_model=ProjectTranslationDetailDisplayAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def add_project_videos_admin(
    req: Request,
    project_id: UUID,
    default_language: str = Form(default=default_lang()),
    project_videos: List[UploadFile] = File(None),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    project = await projects.add_project_videos_admin(
        req,
        project_id,
        default_language,
        project_videos,
        tkn,
        db,
    )
    return project


@router.put(
    "/admin/{project_id}/update_project_video/{project_video_id}",
    response_model=ProjectTranslationDetailDisplayAdmin,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_project_video_admin(
    req: Request,
    project_id: UUID,
    project_video_id: UUID,
    new_project_video: UploadFile = File(...),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    project = projects.update_project_video_admin(
        req,
        project_id,
        project_video_id,
        new_project_video,
        tkn,
        db,
    )
    return project


@router.delete(
    "/admin/{project_id}/delete_project_video/{project_video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project_video_admin(
    project_id: UUID,
    project_video_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    projects.delete_project_video_admin(
        project_id,
        project_video_id,
        tkn,
        db,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/admin/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_admin(
    project_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    projects.delete_project_admin(project_id, db, tkn)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
