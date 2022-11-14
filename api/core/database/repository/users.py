from uuid import UUID

from core.additional_helpers import data_with_deleted_empty_fields
from core.additional_helpers import replace_and_save_img_to_thumbnail
from core.additional_helpers import save_uploaded_file_and_return_file_path
from core.additional_helpers import static_users_dir_name
from core.additional_helpers import USERS
from core.database.base.query_helpers import DbQuery
from core.database.models.users import User
from core.exceptions import exceptions
from core.security import FieldsValidations
from core.security import Password
from core.security import Tkn
from fastapi import Request
from fastapi import UploadFile
from sqlalchemy.orm.session import Session


def get_all_users(tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_and_super_user_or_exc(tkn, db)
    all_users = DbQuery.get_all_items_admin(db, User)
    return all_users


def info_about_user(tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    user = Tkn.user(tkn, User, db)
    if user:
        return user
    else:
        raise exceptions.exception_not_found("User")


def update_user(
    req: Request,
    user_id: UUID,
    username: str,
    avatar: UploadFile,
    old_password: str,
    new_password: str,
    new_password_confirm: str,
    is_active: bool,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    user = DbQuery.get_one_user_by_user_id(db, user_id, User)
    all_data = {
        "username": username,
        "avatar": avatar,
        "old_password": old_password,
        "password": new_password,
        "password_confirm": new_password_confirm,
        "is_active": is_active,
    }
    data = data_with_deleted_empty_fields(all_data, is_active)
    if avatar:
        image_types = USERS.get("allowed_image_types")
        image_size = USERS.get("allowed_image_size")

        if avatar.content_type not in image_types:
            raise exceptions.exception_incorrect_content_type(
                image_types, "avatar"
            )
        if not FieldsValidations.correct_file_size(req, image_size):
            raise exceptions.exception_uploading_file_to_large(image_size)
        user = DbQuery.get_one_active_user_by_user_id(db, user_id, User)

        file_for_save = save_uploaded_file_and_return_file_path(
            user.username,
            static_users_dir_name(),
            avatar.filename,
            avatar.file,
        )

        replace_and_save_img_to_thumbnail(file_for_save)

        data["avatar"] = file_for_save

    if old_password or new_password or new_password_confirm:
        if old_password and new_password and new_password_confirm:
            Password.exception_old_and_new_password_equals(
                old_password, new_password
            )
            Password.exception_correct_new_password_with_confirmation(
                new_password, new_password_confirm
            )
            Password.exception_wrong_password(
                old_password, user.hashed_password
            )
            del data["old_password"]
            del data["password"]
            del data["password_confirm"]
            data["hashed_password"] = Password.hashing_password(new_password)
        else:
            raise exceptions.exception_change_password()

    if Tkn.is_access_tkn_and_active_user_and_super_user(tkn, db):
        if user_id != Tkn.user_id(tkn, User, db):
            user = DbQuery.update_one_user_by_super_user(
                data, db, user_id, User
            )
            return user
        else:
            raise exceptions.exception_not_permissions()

    elif Tkn.is_access_tkn_and_active_user(tkn, db):
        if user_id == Tkn.user_id(tkn, User, db):
            user = DbQuery.update_one_user_username(data, db, user_id, User)
            return user
        else:
            raise exceptions.exception_not_permissions()


def delete_user(tkn: str, user_id: UUID, db: Session):
    Tkn.is_access_tkn_and_active_user_and_super_user_or_exc(tkn, db)
    super_user = Tkn.super_user(tkn, User, db)
    if user_id == super_user.id:
        raise exceptions.exception_can_not_delete_yourself()
    else:
        DbQuery.delete_one_item_by_id_admin(db, user_id, User)
