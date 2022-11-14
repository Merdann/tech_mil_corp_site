from uuid import UUID

from core.additional_helpers import data_with_deleted_empty_fields
from core.additional_helpers import get_capitalize_title
from core.additional_helpers import get_lowercase_title
from core.database.base.query_helpers import DbQuery
from core.database.models.languages import Language
from core.database.models.users import User
from core.exceptions import exceptions
from core.security import Tkn
from sqlalchemy.orm.session import Session


def default_lang():
    return "en"


def get_all_languages_client(db: Session):
    all_languages = DbQuery.get_all_items_client(db, Language)
    return all_languages


def create_language(name: str, code: str, tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    lang_exists = (
        db.query(Language)
        .filter(
            Language.is_deleted == bool(0),
            Language.name == get_capitalize_title(name),
            Language.code == get_lowercase_title(code),
        )
        .first()
    )
    if lang_exists:
        raise exceptions.exception_already_exists("Language or Code")

    language = (
        db.query(Language)
        .filter(
            Language.is_deleted == bool(1),
            Language.code == get_lowercase_title(code),
        )
        .first()
    )
    if language:
        language.is_deleted = False
        language.deleted_at = None
        db.commit()
        db.refresh(language)
    else:
        user_id = Tkn.user_id(tkn, User, db)

        language = Language(
            owner_id=user_id,
            name=get_capitalize_title(name),
            code=get_lowercase_title(code),
        )
        db.add(language)
        db.commit()
        db.refresh(language)

    return language


def get_all_languages(db: Session, tkn: str):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    all_languages = DbQuery.get_all_items_admin(db, Language)
    return all_languages


def get_one_language(language_id: UUID, db: Session, tkn: str):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    language = DbQuery.get_one_item_by_id_admin(db, language_id, Language)
    return language


def update_language(
    language_id: UUID,
    name: str,
    is_active: bool,
    db: Session,
    tkn: str,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    if name:
        name = get_capitalize_title(name)
    language = DbQuery.get_one_item_by_id_admin(db, language_id, Language)
    all_data = {"name": name, "is_active": is_active}

    data = data_with_deleted_empty_fields(all_data, is_active)

    language = DbQuery.update_exists_item_by_id_admin(
        data, db, language_id, Language
    )

    return language


def delete_language(language_id: int, db: Session, tkn: str):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    DbQuery.delete_one_item_by_id_admin(db, language_id, Language)
