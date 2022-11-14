from typing import List
from uuid import UUID

from core.database.base.session import get_db
from core.database.repository import languages
from core.schemas.languages import LanguageDetailDisplay
from core.schemas.languages import LanguageListDisplay
from core.security import JWTBearer
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Response
from fastapi import status
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.get(
    "/all",
    response_model=List[LanguageListDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_languages_client(db: Session = Depends(get_db)):
    all_languages = languages.get_all_languages_client(db)
    return all_languages


@router.post(
    "/admin/create",
    response_model=LanguageDetailDisplay,
    status_code=status.HTTP_201_CREATED,
)
async def create_language(
    name: str = Form(min_length=3, max_length=30),
    code: str = Form(min_length=2, max_length=2),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    language = languages.create_language(name, code, tkn, db)
    return language


@router.get(
    "/admin/all",
    response_model=List[LanguageListDisplay],
    status_code=status.HTTP_200_OK,
)
async def get_all_languages(
    tkn: str = Depends(JWTBearer()), db: Session = Depends(get_db)
):
    all_languages = languages.get_all_languages(db, tkn)
    return all_languages


@router.get(
    "/admin/{language_id}",
    response_model=LanguageDetailDisplay,
    status_code=status.HTTP_200_OK,
)
async def get_one_language(
    language_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    language = languages.get_one_language(language_id, db, tkn)
    return language


@router.put(
    "/admin/{language_id}",
    response_model=LanguageDetailDisplay,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_language(
    language_id: UUID,
    name: str = Form(min_length=3, max_length=30, default=None),
    is_active: bool = Form(True),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    language = languages.update_language(language_id, name, is_active, db, tkn)
    return language


@router.delete("/admin/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_language(
    language_id: UUID,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    languages.delete_language(language_id, db, tkn)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
