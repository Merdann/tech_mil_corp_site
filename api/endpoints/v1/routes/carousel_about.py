from typing import List
from uuid import UUID

from core.database.base.session import get_db
from core.database.repository import carousel_about
from core.schemas.carousel_about import CarouselAboutDisplayClient
from core.schemas.carousel_about import CarouselAboutDisplay
from core.schemas.carousel_about import CarouselAboutDetailDisplayAdmin
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
    response_model=List[CarouselAboutDisplayClient],
    status_code=status.HTTP_200_OK,
)
async def get_all_items_client(
    db: Session = Depends(get_db)
):
    all = carousel_about.get_all_items_client(db)
    return all


@router.post(
    "/admin/create",
    response_model=CarouselAboutDetailDisplayAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def create_element_admin(
    req: Request,
    image: UploadFile = File(...),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    item = await carousel_about.create_element_admin(
        req, image, tkn, db
    )
    return item


@router.get(
    "/admin/all",
    response_model=List[CarouselAboutDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_items_admin(
    tkn: str = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    all = carousel_about.get_all_items_admin(tkn, db)
    return all


@router.get(
    "/admin/{item_id}",
    response_model=CarouselAboutDetailDisplayAdmin,
    status_code=status.HTTP_200_OK,
)
async def get_one_item_admin(
    item_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    item = carousel_about.get_one_item_admin(
        item_id, tkn, db
    )
    return item


@router.put(
    "/admin/{item_id}",
    response_model=CarouselAboutDetailDisplayAdmin,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_courusel_admin(
    req: Request,
    item_id: UUID,
    image: UploadFile = File(None),
    is_active: bool = Form(True),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    item = carousel_about.update_courusel_admin(
        req, item_id, image, is_active, tkn, db
    )
    return item


@router.delete("/admin/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_item_admin(
    item_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    carousel_about.delete_one_item_admin(item_id, tkn, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
