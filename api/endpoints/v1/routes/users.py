from typing import List
from uuid import UUID

from core.database.base.session import get_db
from core.database.repository import users
from core.schemas.users import UserDisplay
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
    "/admin/all",
    response_model=List[UserDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    tkn: str = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    all_users = users.get_all_users(tkn, db)
    return all_users


@router.get(
    "/admin/me", response_model=UserDisplay, status_code=status.HTTP_200_OK
)
async def info_about_user(
    tkn: str = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    user = users.info_about_user(tkn, db)
    return user


@router.put(
    "/admin/{user_id}",
    response_model=UserDisplay,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user(
    req: Request,
    user_id: UUID,
    username: str = Form(min_length=3, max_length=50, default=None),
    avatar: UploadFile = File(None),
    old_password: str = Form(min_length=8, max_length=20, default=None),
    new_password: str = Form(min_length=8, max_length=20, default=None),
    new_password_confirm: str = Form(
        min_length=8, max_length=20, default=None
    ),
    is_active: bool = Form(True),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    user = users.update_user(
        req,
        user_id,
        username,
        avatar,
        old_password,
        new_password,
        new_password_confirm,
        is_active,
        tkn,
        db,
    )
    return user


@router.delete("/admin/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    users.delete_user(tkn, user_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
