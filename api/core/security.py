import re
from datetime import datetime
from datetime import timedelta
from typing import Optional
from uuid import UUID

import jwt
from core.config import settings
from core.database.base.session import SessionLocal
from core.database.models.users import BlacklistedJWTS
from core.database.models.users import User
from core.exceptions import exceptions
from core.schemas.authentication import AccessTokenForGetRefreshTokenBase
from cryptography.hazmat.primitives import serialization
from fastapi import HTTPException
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session


class FieldsValidations:
    @staticmethod
    def correct_email(email):
        p = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        return bool(re.fullmatch(p, email))

    @staticmethod
    def correct_phone(phone):
        p = r"(\+9936[0-5][\d]{6})"
        return bool(re.fullmatch(p, phone))

    @staticmethod
    def correct_file_size(request, file_size):
        if float(request.headers.get("content-length")) <= file_size:
            return True


class Password:

    pwd_cntxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hashing_password(password):
        return Password.pwd_cntxt.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return Password.pwd_cntxt.verify(plain_password, hashed_password)

    @staticmethod
    def correct_password(plain_password):
        p = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$"
        return bool(re.fullmatch(p, plain_password))

    @staticmethod
    def exception_wrong_password(plain_password, hashed_password):
        if not Password.verify_password(plain_password, hashed_password):
            raise exceptions.exception_wrong_password()

    @staticmethod
    def exception_old_and_new_password_equals(old_password, new_password):
        if old_password == new_password:
            raise exceptions.exception_old_and_new_password_equals()

    @staticmethod
    def exception_correct_new_password_with_confirmation(
        password, password_confirm
    ):
        if password != password_confirm:
            raise exceptions.exception_passwords_does_not_match()
        if 20 < len(password) < 8:
            raise exceptions.exception_password_is_too_short_or_long(8, 20)
        if not Password.correct_password(password):
            raise exceptions.exception_password_is_too_easy()


class Tkn:

    priv_key = settings.JWT_PRIVATE_KEY
    priv_key_ser = serialization.load_ssh_private_key(
        priv_key.encode(), password=b""
    )
    pub_key = settings.JWT_PUBLIC_KEY
    pub_key_ser = serialization.load_ssh_public_key(pub_key.encode())

    @staticmethod
    def encode_token(payload, exp_delta: Optional[timedelta] = None):
        to_encode = payload.copy()
        if exp_delta:
            exp = datetime.now() + exp_delta
        else:
            exp = datetime.now() + timedelta(minutes=settings.TKN_EXP_MINS)
        created = datetime.now().isoformat()
        to_encode.update(
            {
                "created": created,
                "exp": exp,
            }
        )
        encoded = jwt.encode(
            payload=to_encode,
            key=Tkn.priv_key_ser,
            algorithm=settings.ALGORITHM,
        )
        return encoded

    @staticmethod
    def decode_token(token):
        try:
            decoded = jwt.decode(
                jwt=token, key=Tkn.pub_key_ser, algorithms=[settings.ALGORITHM]
            )
            return decoded
        except jwt.exceptions.DecodeError:
            raise exceptions.exception_token_decode_error()

    @staticmethod
    def data_in_token(token):
        data = Tkn.decode_token(token)
        return data

    @staticmethod
    def is_super_user(tkn: str, db: Session):
        user_id = Tkn.data_in_token(tkn).get("user_id")
        user_name = Tkn.data_in_token(tkn).get("user_name")
        user = (
            db.query(User)
            .filter(
                User.id == user_id,
                User.username == user_name,
                User.is_active == bool(1),
                User.is_deleted == bool(0),
                User.is_superuser == bool(1),
            )
            .first()
        )
        if user:
            return True
        else:
            return False

    @staticmethod
    def is_super_user_or_exception(tkn: str, db: Session):
        user = Tkn.is_super_user(tkn, db)
        if user:
            return True
        else:
            raise exceptions.exception_not_permissions()

    @staticmethod
    def is_active_user(tkn: str, db: Session):
        user_id = Tkn.data_in_token(tkn).get("user_id")
        user = (
            db.query(User)
            .filter(
                User.is_deleted == bool(0),
                User.is_active == bool(1),
                User.id == user_id,
            )
            .first()
        )
        if user:
            return True
        else:
            return False

    @staticmethod
    def is_active_user_or_exception(tkn: str, db: Session):
        user = Tkn.is_active_user(tkn, db)
        if user:
            return True
        else:
            raise exceptions.exception_not_permissions()

    @staticmethod
    def get_is_jwt_in_blacklist(db: Session, tkn: str, user_id: UUID):
        item = (
            db.query(BlacklistedJWTS)
            .filter(
                BlacklistedJWTS.is_deleted == bool(0),
                BlacklistedJWTS.is_active == bool(1),
                BlacklistedJWTS.user_id == user_id,
                BlacklistedJWTS.jwt == tkn,
            )
            .first()
        )
        if item:
            return True
        else:
            return False

    @staticmethod
    def is_access_token(tkn: str, db: Session):
        access_elements = ["user_id", "user_name", "exp", "created"]
        tkn_data = Tkn.data_in_token(tkn)
        user_id = Tkn.data_in_token(tkn).get("user_id")
        tkn_blacklist = Tkn.get_is_jwt_in_blacklist(db, tkn, user_id)
        if set(access_elements) == set(tkn_data) and not tkn_blacklist:
            return True
        else:
            return False

    @staticmethod
    def is_access_token_or_exception(tkn: str, db: Session):
        access_token = Tkn.is_access_token(tkn, db)
        if access_token:
            return True
        else:
            raise exceptions.exception_not_permissions()

    @staticmethod
    def is_refresh_token(
        tkn: str, db: Session, request: AccessTokenForGetRefreshTokenBase
    ):
        refresh_elements = ["user_id", "exp", "created"]
        tkn_data = Tkn.data_in_token(tkn)
        if type(request) == str:
            user_id = Tkn.data_in_token(request).get("user_id")
            tkn_blacklist = Tkn.get_is_jwt_in_blacklist(db, tkn, user_id)
        elif type(request) == dict:
            user_id = Tkn.data_in_token(request["access_token"]).get("user_id")
            tkn_blacklist = Tkn.get_is_jwt_in_blacklist(db, tkn, user_id)
        else:
            user_id = Tkn.data_in_token(request.access_token).get("user_id")
            tkn_blacklist = Tkn.get_is_jwt_in_blacklist(db, tkn, user_id)
        if set(refresh_elements) == set(tkn_data) and not tkn_blacklist:
            return True
        else:
            return False

    @staticmethod
    def is_refresh_token_or_exception(
        tkn: str, db: Session, request: AccessTokenForGetRefreshTokenBase
    ):
        refresh_token = Tkn.is_refresh_token(tkn, db, request)

        if refresh_token:
            return True
        else:
            raise exceptions.exception_not_permissions()

    @staticmethod
    def is_access_tkn_and_active_user_and_super_user(tkn: str, db: Session):
        if (
            Tkn.is_access_token(tkn, db)
            and Tkn.is_active_user(tkn, db)
            and Tkn.is_super_user(tkn, db)
        ):
            return True
        else:
            return False

    @staticmethod
    def is_access_tkn_and_active_user_and_super_user_or_exc(
        tkn: str, db: Session
    ):
        if Tkn.is_access_tkn_and_active_user_and_super_user(tkn, db):
            return True
        else:
            raise exceptions.exception_not_permissions()

    @staticmethod
    def is_access_tkn_and_active_user(tkn: str, db: Session):
        if Tkn.is_access_token(tkn, db) and Tkn.is_active_user(tkn, db):
            return True
        else:
            return False

    @staticmethod
    def is_access_tkn_and_active_user_or_exc(tkn: str, db: Session):
        if Tkn.is_access_tkn_and_active_user(tkn, db):
            return True
        else:
            raise exceptions.exception_not_permissions()

    @staticmethod
    def is_refresh_tkn_and_active_user(
        tkn: str, db: Session, request: AccessTokenForGetRefreshTokenBase
    ):
        if Tkn.is_refresh_token(tkn, db, request) and Tkn.is_active_user(
            tkn, db
        ):
            return True
        else:
            return False

    @staticmethod
    def is_refresh_tkn_and_active_user_or_exc(
        tkn: str, db: Session, request: AccessTokenForGetRefreshTokenBase
    ):
        if Tkn.is_refresh_tkn_and_active_user(tkn, db, request):
            return True
        else:
            raise exceptions.exception_not_permissions()

    @staticmethod
    def user(token, model, db):
        user_id = Tkn.data_in_token(token).get("user_id")
        user = (
            db.query(model)
            .filter(
                model.id == user_id,
                model.is_active == bool(1),
                model.is_deleted == bool(0),
            )
            .first()
        )
        return user

    # @staticmethod
    # def user(token, model, db):
    #     user_id = Tkn.data_in_token(token).get("user_id")
    #     user_name = Tkn.data_in_token(token).get("user_name")
    #     user = (
    #         db.query(model)
    #         .filter(
    #             model.id == user_id,
    #             model.username == user_name,
    #             model.is_active == bool(1),
    #             model.is_deleted == bool(0),
    #         )
    #         .first()
    #     )
    #     return user

    @staticmethod
    def super_user(token, model, db):
        user_id = Tkn.data_in_token(token).get("user_id")
        user_name = Tkn.data_in_token(token).get("user_name")
        user = (
            db.query(model)
            .filter(
                model.id == user_id,
                model.username == user_name,
                model.is_active == bool(1),
                model.is_deleted == bool(0),
                model.is_superuser == bool(1),
            )
            .first()
        )
        return user

    @staticmethod
    def user_id(token, model, db):
        user_id_from_tkn = Tkn.data_in_token(token).get("user_id")
        user = (
            db.query(model)
            .filter(
                model.id == user_id_from_tkn,
                model.is_active == bool(1),
                model.is_deleted == bool(0),
            )
            .first()
        )
        user_id = user.id
        return user_id


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = Tkn.decode_token(jwtoken)
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


class AuthStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:
        assert scope["type"] == "http"
        request = Request(scope, receive)
        await AuthStaticFiles.verify_token(request)
        await super().__call__(scope, receive, send)

    @staticmethod
    async def verify_token(request: Request) -> HTTPAuthorizationCredentials:
        db = SessionLocal()
        security = HTTPBearer()
        credentials = await security(request)
        path = request.url.path
        users = "/static/images/users/"

        if path.startswith(users):
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(
                        status_code=403,
                        detail="Invalid authentication scheme.",
                    )
                if not Tkn.is_access_tkn_and_active_user(
                    credentials.credentials, db
                ):
                    raise HTTPException(
                        status_code=403,
                        detail="Invalid token or expired token.",
                    )
                return True
            else:
                raise HTTPException(
                    status_code=403, detail="Invalid authorization code."
                )
        else:
            return True
