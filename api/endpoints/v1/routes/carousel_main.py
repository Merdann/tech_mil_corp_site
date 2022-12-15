from typing import List
from typing import Optional
from uuid import UUID

from core.database.base.session import get_db
from core.database.repository import carousel_main
from core.database.repository.languages import default_lang
from core.schemas.carousel_main import CarouselMainDisplayClient
from core.schemas.carousel_main import CarouselMainDisplay
from core.schemas.carousel_main import CarouselMainDetailDisplayAdmin
from core.security import JWTBearer
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination import paginate
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.get(
    "/all",
    response_model=List[CarouselMainDisplayClient],
    status_code=status.HTTP_200_OK,
)
async def get_all_items_client(
    db: Session = Depends(get_db)
):
    all = carousel_main.get_all_items_client(db)
    return all


@router.post(
    "/admin/create",
    response_model=CarouselMainDetailDisplayAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def create_element_admin(
    req: Request,
    image: UploadFile = File(...),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    item = await carousel_main.create_element_admin(
        req, image, tkn, db
    )
    return item


@router.get(
    "/admin/all",
    response_model=List[CarouselMainDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_items_admin(
    tkn: str = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    all = carousel_main.get_all_items_admin(tkn, db)
    return all


@router.get(
    "/admin/{item_id}",
    response_model=CarouselMainDetailDisplayAdmin,
    status_code=status.HTTP_200_OK,
)
async def get_one_item_admin(
    item_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    item = carousel_main.get_one_item_admin(
        item_id, tkn, db
    )
    return item


@router.put(
    "/admin/{item_id}",
    response_model=CarouselMainDetailDisplayAdmin,
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
    item = carousel_main.update_courusel_admin(
        req, item_id, image, is_active, tkn, db
    )
    return item


@router.delete("/admin/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_item_admin(
    item_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    carousel_main.delete_one_item_admin(item_id, tkn, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
