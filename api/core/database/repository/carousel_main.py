from uuid import UUID

from core.additional_helpers import COURUSEL
from core.additional_helpers import static_courusel_dir_name
from core.additional_helpers import data_with_deleted_empty_fields
from core.additional_helpers import prepare_file_for_save
from core.database.base.query_helpers import DbQuery
from core.database.models.carousel_main import CarouselMain
from core.exceptions import exceptions
from core.security import Tkn
from fastapi import Request
from fastapi import UploadFile
from sqlalchemy.orm.session import Session


def get_all_items_client(db: Session):
    all = DbQuery.get_all_items_client(
        db, CarouselMain
    )
    return all


async def create_element_admin(
    req: Request,
    image: UploadFile,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    exceptions.exception_by_checking_file_types_and_size(
        req,
        image,
        COURUSEL.get("allowed_image_types"),
        COURUSEL.get("allowed_image_size"),
    )

    file_for_save = prepare_file_for_save(
        image.filename, static_courusel_dir_name(), image
    )

    data = {
        "image": file_for_save,
    }

    element = await DbQuery.create_element(db, tkn, CarouselMain, data)

    return element


def get_all_items_admin(tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    all = DbQuery.get_all_items_admin(db, CarouselMain)
    return all


def get_one_item_admin(item_id: UUID, tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    item = DbQuery.get_one_item_by_id_admin(db, item_id, CarouselMain)
    return item


def update_courusel_admin(
    req: Request,
    item_id: UUID,
    image: UploadFile,
    is_active: bool,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    data = data_with_deleted_empty_fields(
        {
            "is_active": is_active,
        },
        is_active,
    )
    if image:
        exceptions.exception_by_checking_file_types_and_size(
            req,
            image,
            COURUSEL.get("allowed_image_types"),
            COURUSEL.get("allowed_image_size"),
        )
        file_for_save = prepare_file_for_save(
            image.filename, static_courusel_dir_name(), image
        )
        data["image"] = file_for_save
        item = DbQuery.update_exists_item_by_id_admin(
            data, db, item_id, CarouselMain)
    item = DbQuery.update_exists_item_by_id_admin(
        data, db, item_id, CarouselMain)

    return item


def delete_one_item_admin(item_id: UUID, tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    DbQuery.delete_one_item_by_id_admin(db, item_id, CarouselMain)
