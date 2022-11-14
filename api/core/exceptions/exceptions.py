import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

import ujson
from core.security import FieldsValidations
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from starlette.background import BackgroundTask


class CustomResponse(JSONResponse):
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Optional[dict] = None,
        media_type: Optional[str] = None,
        background: Optional[BackgroundTask] = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    @staticmethod
    def data_repr(
        message: str = "", errors: List = [], data: Union[Dict, List] = {}
    ):
        data = {"message": message, "errors": errors, "data": data}
        return data

    def render(self, content: Any) -> bytes:
        return ujson.dumps(content).encode("utf-8")


def exception_field_is_required(field, field_name: str):
    if not field:
        msg = f"{field_name.capitalize()} field is required"
        logging.warning("\n" + msg)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


def exception_wrong_svg_format(svg_code: str):
    if svg_code.startswith("<svg") and svg_code.endswith("</svg>"):
        return False
    return True


def exception_svg():
    msg = "SVG must be start with '<svg' and end with '</svg>'"
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=msg,
    )


def exception_can_not_delete_yourself():
    msg = "You do not have permission to delete yourself."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=msg,
    )


def exception_not_permissions():
    msg = "You do not have permission to do this action."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=msg,
    )


def exception_something_went_wrong():
    msg = "Something went wrong."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_not_found(item: str):
    msg = f"{item} not found."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=msg,
    )


def exception_already_exists(item: str):
    msg = f"{item} already exists."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_change_password():
    msg = "If you wanna change your password you must set correct "
    "old password, new_password and new_password_confirm."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_invalid_credentials():
    msg = "Wrong username or password."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_wrong_password():
    msg = "Wrong password."
    logging.warning("\n" + msg)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


def exception_old_and_new_password_equals():
    msg = "Old password and new password can't be same."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_token_decode_error():
    msg = "Token decoding error."
    logging.warning("\n" + msg)
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg)


def exception_passwords_does_not_match():
    msg = "Password and Password Confirmation doesn't match."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_incorrect_old_password():
    msg = "Your Old Password incorrect."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_username_is_too_short(min_len, max_len):
    msg = f"Username must be more than {min_len} "
    f"and less than {max_len} charecters."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_password_is_too_short_or_long(min_len, max_len):
    msg = f"Password must be more than {min_len} "
    f"and less than {max_len} charecters."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_password_is_too_easy():
    msg = "Password is too easy to guess."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_incorrect_email():
    msg = "Incorrect email format. Please enter correct email address."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_incorrect_phone_number():
    msg = "Incorrect phone number format. Please enter correct phone."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_incorrect_content_type(list_of_types: List, field: str = "this"):
    types = ", ".join([i.split("/")[-1] for i in list_of_types])
    msg = f"You can upload only {types} "
    f"file type/s in {field} field/s."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_uploading_file_to_large(file_size: int):
    size = float(file_size / 1000000)
    msg = f"You can't upload file(s) with size more than {size} MB."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail=msg,
    )


def exception_can_not_delete_tag_related_with_project():
    msg = "You can't delete tag related with project."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_can_not_set_next_values(value: int, list_of_values: List[int]):
    msg = f"Max value you can set to this field is [{value}] "
    f"and you can't set next values {list_of_values} to this field."
    logging.warning("\n" + msg)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )


def exception_if_elem_already_exists(db: Session, table, title: str):
    element_exists = (
        db.query(table)
        .filter(
            table.is_deleted == bool(0),
            table.title == title,
            table.origin_lang_code == "en",
        )
        .first()
    )
    if element_exists:
        raise exception_already_exists(table.__tablename__)


def exception_if_not_origin_elem_id(origin_elem_id: UUID):
    if not origin_elem_id:
        raise exception_something_went_wrong()


def exception_if_origin_elem_does_not_exists(
    db: Session, table, origin_elem_id: UUID
):
    element_exists = (
        db.query(table)
        .filter(table.is_deleted == bool(0), table.id == origin_elem_id)
        .first()
    )
    if not element_exists:
        raise exception_not_found(table.__tablename__)


def exception_if_translated_elem_already_exists(
    db: Session, table, lang_code: str, origin_elem_id: UUID
):
    translation_exists = (
        db.query(table)
        .filter(
            table.is_deleted == bool(0),
            table.lang_code == lang_code,
            table.origin_elem_id == origin_elem_id,
        )
        .first()
    )
    if translation_exists:
        raise exception_already_exists(table.__tablename__)


def exception_by_checking_file_types_and_size(
    req, file, file_types, file_size
):
    if file.content_type not in file_types:
        raise exception_incorrect_content_type(file_types, "field")
    if not FieldsValidations.correct_file_size(req, file_size):
        raise exception_uploading_file_to_large(file_size)


def exception_by_checking_file_types(file, file_types):
    if file.content_type not in file_types:
        raise exception_incorrect_content_type(file_types, "field")


def exception_by_checking_file_size(req, file_size):
    if not FieldsValidations.correct_file_size(req, file_size):
        raise exception_uploading_file_to_large(file_size)


def exception_by_compare_file_size(uploaded_file_size, allowed_file_size):
    if uploaded_file_size > allowed_file_size:
        raise exception_uploading_file_to_large(allowed_file_size)
