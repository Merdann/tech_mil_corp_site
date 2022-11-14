from typing import List
from uuid import UUID

from core.database.base.session import get_db
from core.database.repository import follow_us
from core.schemas.follow_us import FollowUsDisplay
from core.security import JWTBearer
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Response
from fastapi import status
from pydantic import EmailStr
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.post(
    "/follow",
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_info_with_email(
    email: EmailStr = Form(...),
    db: Session = Depends(get_db),
):
    item = await follow_us.post_info_with_email(email, db)
    return item


@router.get(
    "/admin/follow/all",
    response_model=List[FollowUsDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_followed_emails_admin(
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    items = await follow_us.get_all_followed_emails_admin(tkn, db)
    return items


@router.delete("/admin/{follower_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_follower_admin(
    follower_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    follow_us.delete_follower_admin(follower_id, tkn, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
