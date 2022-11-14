from typing import List
from uuid import UUID

from core.database.base.session import get_db
from core.database.repository import main_video
from core.schemas.main_video import MainVideoDisplay
from core.schemas.main_video import MainVideoDisplayAdmin
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
    response_model=List[MainVideoDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_main_video_client(db: Session = Depends(get_db)):
    video = main_video.get_main_video_client(db)
    return video


@router.post(
    "/admin/create",
    response_model=MainVideoDisplayAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def create_main_video(
    req: Request,
    video: UploadFile = File(...),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    video = main_video.create_main_video(
        req,
        video,
        tkn,
        db,
    )
    return video


@router.get(
    "/admin/all",
    response_model=List[MainVideoDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_main_video_admin(
    tkn: str = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    video = main_video.get_main_video_admin(tkn, db)
    return video


@router.get(
    "/admin/{video_id}",
    response_model=MainVideoDisplayAdmin,
    status_code=status.HTTP_200_OK,
)
async def get_one_video_admin(
    video_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    video = main_video.get_one_video_admin(video_id, tkn, db)
    return video


@router.put(
    "/admin/{video_id}",
    response_model=MainVideoDisplayAdmin,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_video_admin(
    video_id: UUID,
    req: Request,
    video: UploadFile = File(None),
    is_active: bool = Form(True),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    video = main_video.update_video_admin(
        video_id,
        req,
        video,
        is_active,
        tkn,
        db,
    )
    return video


@router.delete("/admin/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video_admin(
    video_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    main_video.delete_video_admin(video_id, tkn, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
