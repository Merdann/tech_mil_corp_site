from core.database.base.session import get_db
from core.database.repository import authentication
from core.schemas.authentication import AccessRefreshTokenDisplay
from core.security import JWTBearer
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi import Response
from fastapi import status
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.post(
    "/admin/sign_in",
    response_model=AccessRefreshTokenDisplay,
    status_code=status.HTTP_200_OK,
)
async def sign_in_user(
    req: Request,
    username: str = Form(min_length=3, max_length=50),
    password: str = Form(min_length=8, max_length=20),
    db: Session = Depends(get_db),
):
    user = authentication.sign_in_user(username, password, db)
    return user


@router.post(
    "/admin/sign_up",
    response_model=AccessRefreshTokenDisplay,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up_user(
    username: str = Form(min_length=3, max_length=50),
    password: str = Form(min_length=8, max_length=20),
    password_confirm: str = Form(min_length=8, max_length=20),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    user = authentication.sign_up_user(
        username, password, password_confirm, tkn, db
    )
    return user


@router.get("/admin/sign_out", status_code=status.HTTP_204_NO_CONTENT)
async def sign_out_user(
    req: Request,
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    authentication.sign_out_user(tkn, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/admin/refresh",
    response_model=AccessRefreshTokenDisplay,
    status_code=status.HTTP_200_OK,
)
async def get_access_token_by_refresh_token(
    access_token: str = Form(...),
    tkn: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    upd_tkns = authentication.get_access_token_by_refresh_token(
        access_token, tkn, db
    )
    return upd_tkns
