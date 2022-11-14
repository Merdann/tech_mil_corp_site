from datetime import datetime
from datetime import timedelta

from core.additional_helpers import default_images_for_fixtures_dir_name
from core.additional_helpers import dir_with_file_for_save_path
from core.additional_helpers import static_users_dir_name
from core.config import settings
from core.database.base.query_helpers import DbQuery
from core.database.models.users import BlacklistedJWTS
from core.database.models.users import User
from core.exceptions import exceptions
from core.security import Password
from core.security import Tkn
from PIL import Image
from sqlalchemy.orm.session import Session


def sign_in_user(username: str, password: str, db: Session):
    user = DbQuery.get_one_active_user_by_user_name(db, username, User)
    if not Password.verify_password(password, user.hashed_password):
        raise exceptions.exception_invalid_credentials()
    access_token = Tkn.encode_token(
        {"user_id": str(user.id), "user_name": user.username},
        exp_delta=timedelta(minutes=settings.ACCES_TKN_EXP_MINS),
    )
    refresh_token = Tkn.encode_token(
        {"user_id": str(user.id)},
        exp_delta=timedelta(days=settings.REFRESH_TKN_EXP_DAYS),
    )
    tokens = {"access_token": access_token, "refresh_token": refresh_token}

    return tokens


def sign_up_user(
    username: str, password: str, password_confirm: str, tkn: str, db: Session
):
    Tkn.is_super_user_or_exception(tkn, db)
    user_exists = DbQuery.get_one_user_by_user_name_deleted_too_exceptionless(
        db, username, User
    )
    if user_exists:
        raise exceptions.exception_already_exists("User")
    if 50 < len(username) < 3:
        raise exceptions.exception_username_is_too_short(3, 50)

    Password.exception_correct_new_password_with_confirmation(
        password, password_confirm
    )

    file_name_simplusr = "default_user_avatar.png"

    file_simplusr = (
        f"{default_images_for_fixtures_dir_name()}/{file_name_simplusr}"
    )

    simple_file_path_to_save = dir_with_file_for_save_path(
        username, static_users_dir_name(), file_name_simplusr
    )

    imgsimplusr = Image.open(file_simplusr)
    imgsimplusr.save(simple_file_path_to_save)
    imgsimplusr.close

    user = User(
        username=username,
        hashed_password=Password.hashing_password(password),
        avatar=simple_file_path_to_save,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = Tkn.encode_token(
        {"user_id": str(user.id), "user_name": user.username},
        exp_delta=timedelta(minutes=settings.ACCES_TKN_EXP_MINS),
    )

    refresh_token = Tkn.encode_token(
        {"user_id": str(user.id)},
        exp_delta=timedelta(days=settings.REFRESH_TKN_EXP_DAYS),
    )

    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens


def sign_out_user(tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    tkn_data = Tkn.data_in_token(tkn)
    user_id = tkn_data.get("user_id", None)
    created = tkn_data.get("created", None)
    exp = tkn_data.get("exp", None)
    tkn_created = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%f")
    tkn_expires = datetime.utcfromtimestamp(exp)
    DbQuery.add_jwt_in_blacklist(
        db, tkn, user_id, tkn_created, tkn_expires, BlacklistedJWTS
    )


def get_access_token_by_refresh_token(
    access_token: str, tkn: str, db: Session
):
    Tkn.is_refresh_tkn_and_active_user_or_exc(tkn, db, access_token)
    tkn_data = Tkn.data_in_token(tkn)
    user_id = tkn_data.get("user_id", None)
    if user_id:
        exs_user = DbQuery.get_one_active_user_by_user_id_exceptionless(
            db, user_id, User
        )
        if exs_user:
            access_token = Tkn.encode_token(
                {
                    "user_id": str(exs_user.id),
                    "user_name": exs_user.username,
                },
                exp_delta=timedelta(minutes=settings.ACCES_TKN_EXP_MINS),
            )
            refresh_token = Tkn.encode_token(
                {"user_id": str(exs_user.id)},
                exp_delta=timedelta(days=settings.REFRESH_TKN_EXP_DAYS),
            )
            updated_tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            return updated_tokens
        else:
            raise exceptions.exception_something_went_wrong()
