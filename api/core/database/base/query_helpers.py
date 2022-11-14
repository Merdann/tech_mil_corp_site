from datetime import datetime
from typing import List

from core.database.models.users import User
from core.exceptions import exceptions
from core.security import Tkn
from sqlalchemy import desc


class DbQuery:
    @staticmethod
    def exception_404(title="Item"):
        return exceptions.exception_not_found(title)

    @staticmethod
    def get_is_jwt_in_blacklist(db, jwt, user_id, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.user_id == user_id,
                model.jwt == jwt,
            )
            .first()
        )
        if item:
            return True
        else:
            return False

    @staticmethod
    def add_jwt_in_blacklist(
        db, tkn, user_id, tkn_created, tkn_expires, model
    ):
        item = model(
            jwt=tkn,
            user_id=user_id,
            jwt_created=tkn_created,
            jwt_expires=tkn_expires,
        )
        db.add(item)
        db.commit()

    @staticmethod
    async def create_element(db, tkn, model, data):
        if tkn:
            user_id = Tkn.user_id(tkn, User, db)
            prepared_data = {"owner_id": user_id}
        else:
            prepared_data = {}
        if type(data) == dict:
            prepared_data.update(data)
        else:
            prepared_data.update(data.dict())
        element = model(**prepared_data)
        db.add(element)
        db.commit()
        db.refresh(element)
        return element

    @staticmethod
    def get_one_active_user_by_user_id(db, user_id, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.id == user_id,
            )
            .first()
        )
        if item is None:
            raise exceptions.exception_not_found("User")
        return item

    @staticmethod
    def get_one_active_user_by_user_id_exceptionless(db, user_id, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.id == user_id,
            )
            .first()
        )
        return item

    @staticmethod
    def get_one_active_user_by_user_name(db, user_name, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.username == user_name,
            )
            .first()
        )
        if item is None:
            raise exceptions.exception_not_found("User")
        return item

    @staticmethod
    def get_one_user_by_user_id(db, user_id, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.id == user_id)
            .first()
        )
        if item is None:
            raise exceptions.exception_not_found("User")
        return item

    @staticmethod
    def get_one_user_by_user_id_for_update(db, user_id, model):
        item = db.query(model).filter(
            model.is_deleted == bool(0), model.id == user_id
        )
        return item

    @staticmethod
    def update_one_user_by_super_user(request, db, user_id, model):
        user = DbQuery.get_one_user_by_user_id_for_update(db, user_id, model)
        if type(request) == dict:
            user.update(request)
        else:
            user.update(request.dict())
        db.commit()
        if user is None:
            raise exceptions.exception_not_found("User")
        return user.first()

    @staticmethod
    def update_one_user_username(request, db, user_id, model):
        user = DbQuery.get_one_user_by_user_id_for_update(db, user_id, model)
        if type(request) == dict:
            del request["is_active"]
            user.update(request)
        else:
            del request.dict()["is_active"]
            user.update(request.dict())
        db.commit()
        if user is None:
            raise exceptions.exception_not_found("User")
        return user.first()

    @staticmethod
    def get_one_user_by_user_name(db, user_name, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.username == user_name)
            .first()
        )
        if item is None:
            raise exceptions.exception_not_found("User")
        return item

    @staticmethod
    def get_one_user_by_user_name_deleted_too_exceptionless(
        db, user_name, model
    ):
        item = db.query(model).filter(model.username == user_name).first()
        return item

    @staticmethod
    def get_one_user_by_user_name_exceptionless(db, user_name, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.username == user_name)
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_table_name_exceptionless_admin(db, table_name, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0), model.table_name == table_name
            )
            .first()
        )
        return item

    @staticmethod
    def get_all_unwatched_by_admin_items_admin(db, model):
        all_items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0), model.watched_by_admin == bool(0)
            )
            .order_by(desc(model.created_at))
            .all()
        )
        return all_items

    @staticmethod
    def get_all_teammates_admin(db, model):
        all_items = (
            db.query(model)
            .filter(model.is_deleted == bool(0))
            .order_by(model.weight)
            .all()
        )
        return all_items

    @staticmethod
    def get_all_teammates_client(db, model):
        all_items = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.is_active == bool(1))
            .order_by(model.weight)
            .all()
        )
        return all_items

    @staticmethod
    def get_all_video_reels_admin(db, model):
        all_items = (
            db.query(model)
            .filter(model.is_deleted == bool(0))
            .order_by(desc(model.year))
            .all()
        )
        return all_items

    @staticmethod
    def get_all_video_reels_client(db, model):
        all_items = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.is_active == bool(1))
            .order_by(desc(model.year))
            .all()
        )
        return all_items

    @staticmethod
    def get_all_items_admin(db, model):
        all_items = (
            db.query(model)
            .filter(model.is_deleted == bool(0))
            .order_by(desc(model.created_at))
            .all()
        )
        return all_items

    @staticmethod
    def get_all_items_client(db, model):
        all_items = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.is_active == bool(1))
            .order_by(desc(model.created_at))
            .all()
        )
        return all_items

    @staticmethod
    def get_all_found_items_by_full_name_admin(db, full_name, model):
        items = (
            db.query(model)
            .filter(model.is_deleted == bool(0))
            .order_by(desc(model.created_at))
            .all()
        )
        found = [
            item
            for item in items
            if full_name.lower() in item.full_name.lower()
        ]
        return found

    @staticmethod
    def get_all_found_items_by_project_title_admin(db, project, model):
        items = (
            db.query(model)
            .filter(model.is_deleted == bool(0))
            .order_by(desc(model.created_at))
            .all()
        )
        found = [
            item
            for item in items
            if project.lower() in item.proj_title.lower()
        ]
        return found

    @staticmethod
    def get_one_item_by_id_and_lang_code_admin(db, item_id, lang_code, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.id == item_id,
                model.lang_code == lang_code,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_id_admin(db, item_id, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.id == item_id)
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_id_exceptionless_admin(db, item_id, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.id == item_id)
            .first()
        )
        return item

    @staticmethod
    def get_all_items_by_lang_client(db, lang, model):
        all_items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.lang_code == lang,
            )
            .order_by(desc(model.created_at))
            .all()
        )
        return all_items

    @staticmethod
    def get_all_items_by_lang_admin(db, lang, model):
        all_items = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.lang_code == lang)
            .order_by(desc(model.created_at))
            .all()
        )
        return all_items

    @staticmethod
    def get_one_item_by_lang_id_client(db, item_id, lang, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.origin_elem_id == item_id,
                model.lang_code == lang,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_lang_id_admin(db, item_id, lang, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == item_id,
                model.lang_code == lang,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_id_client(db, item_id, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.id == item_id,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_id_exceptionless_client(db, item_id, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.id == item_id,
            )
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_code_admin(db, item_code, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.code == item_code)
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_code_exceptionless_admin(db, item_code, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.code == item_code)
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_code_client(db, item_code, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.code == item_code,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_lang_code_exceptionless_admin(db, item_code, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.lang_code == item_code)
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_lang_code_exceptionless_client(db, item_code, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.lang_code == item_code,
            )
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_name_admin(db, item_name, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.name == item_name)
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_name_client(db, item_name, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.name == item_name,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_year_exceptionless_admin(db, item_year, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.year == item_year)
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_email_admin_exceptionless(db, item_email, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.email == item_email)
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_title_admin(db, item_title, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.title == item_title)
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_title_client(db, item_title, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.title == item_title,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_title_exceptionless_admin(db, item_title, model):
        item = (
            db.query(model)
            .filter(model.is_deleted == bool(0), model.title == item_title)
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_title_exceptionless_client(db, item_title, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.title == item_title,
            )
            .first()
        )
        return item

    @staticmethod
    def get_exists_item_by_id_for_update_admin(db, item_id, model):
        exists_item = db.query(model).filter(
            model.is_deleted == bool(0), model.id == item_id
        )
        if exists_item.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return exists_item

    @staticmethod
    def get_exists_item_by_id_for_update_client(db, item_id, model):
        exists_item = db.query(model).filter(
            model.is_deleted == bool(0),
            model.is_active == bool(1),
            model.id == item_id,
        )
        if exists_item.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return exists_item

    @staticmethod
    def update_exists_item_by_id_admin(request, db, item_id, model):
        item = DbQuery.get_exists_item_by_id_for_update_admin(
            db, item_id, model
        )
        if type(request) == dict:
            item.update(request)
        else:
            item.update(request.dict())
        db.commit()
        return item.first()

    @staticmethod
    def update_exists_item_by_id_client(request, db, item_id, model):
        item = DbQuery.get_exists_item_by_id_for_update_client(
            db, item_id, model
        )
        if type(request) == dict:
            item.update(request)
        else:
            item.update(request.dict())
        db.commit()
        return item.first()

    @staticmethod
    def get_exists_item_by_lang_id_for_update_by_lang_admin(
        db, item_id, lang, model
    ):
        exists_item = db.query(model).filter(
            model.is_deleted == bool(0),
            model.origin_elem_id == item_id,
            model.lang_code == lang,
        )
        if exists_item.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return exists_item

    @staticmethod
    def update_exists_item_by_lang_id_admin(request, db, item_id, lang, model):

        item = DbQuery.get_exists_item_by_lang_id_for_update_by_lang_admin(
            db, item_id, lang, model
        )
        if type(request) == dict:
            item.update(request)
        else:
            item.update(request.dict())
        db.commit()
        return item.first()

    @staticmethod
    def delete_one_item_by_id_admin(db, item_id, model):
        item = db.query(model).filter(
            model.is_deleted == bool(0), model.id == item_id
        )
        if item.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        item.update({"deleted_at": datetime.now(), "is_deleted": True})
        db.commit()

    @staticmethod
    def delete_all_items_by_origin_elem_id_admin(db, origin_elem_id, model):
        items = db.query(model).filter(
            model.is_deleted == bool(0), model.origin_elem_id == origin_elem_id
        )
        if items.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        for item in items:
            item.deleted_at = (datetime.now(),)
            item.is_deleted = True
            db.commit()

    @staticmethod
    def delete_one_item_by_id_client(db, item_id, model):
        item = db.query(model).filter(
            model.is_deleted == bool(0),
            model.is_active == bool(1),
            model.id == item_id,
        )
        if item.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        item.update({"deleted_at": datetime.now(), "is_deleted": True})
        db.commit()

    @staticmethod
    def delete_one_item_by_lang_id_admin(db, item_id, lang, model):
        item = db.query(model).filter(
            model.is_deleted == bool(0),
            model.origin_elem_id == item_id,
            model.lang_code == lang,
        )
        if item.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        item.update({"deleted_at": datetime.now(), "is_deleted": True})
        db.commit()

    @staticmethod
    def delete_all_translated_items_by_item_id_admin(db, item_id, model):
        items = db.query(model).filter(
            model.is_deleted == bool(0), model.origin_elem_id == item_id
        )
        if items.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        for item in items:
            item.deleted_at = (datetime.now(),)
            item.is_deleted = True
            db.commit()

    @staticmethod
    def delete_all_images_by_origin_elem_id_admin(db, origin_elem_id, model):
        items = db.query(model).filter(
            model.is_deleted == bool(0), model.origin_elem_id == origin_elem_id
        )
        if items.first():
            for item in items:
                item.deleted_at = (datetime.now(),)
                item.is_deleted = True
                db.commit()

    @staticmethod
    def delete_all_related_items_by_origin_elem_id_admin(
        db, origin_elem_id, models: List
    ):
        for model in models:
            items = db.query(model).filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
            )
            if items.first():
                for item in items:
                    item.deleted_at = (datetime.now(),)
                    item.is_deleted = True
                    db.commit()

    @staticmethod
    def translation_exists(db, model, owner_id, origin_elem_id, lang_code):
        translation = (
            db.query(model)
            .filter(
                model.owner_id == owner_id,
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang_code,
            )
            .first()
        )
        return translation

    @staticmethod
    def get_all_translated_items_by_lang_by_origin_elem_id(
        db, model, lang_code
    ):
        translation = (
            db.query(model)
            .filter(model.lang_code == lang_code)
            .order_by(desc(model.created_at))
            .all()
        )
        return translation

    @staticmethod
    def get_all_ordered_budget_admin(db, model):
        items = (
            db.query(model)
            .filter(model.is_deleted == bool(0))
            .order_by(model.description, model.assuming_sum)
            .all()
        )
        return items

    @staticmethod
    def get_one_item_by_budg_id_and_by_lng_admin(db, budg_id, lang, model):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.budget_id == budg_id,
                model.lang_code == lang,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_origin_elem_and_budg_id_by_lng_admin(
        db, budg_descr_id, budg_id, lang, model
    ):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == budg_descr_id,
                model.budget_id == budg_id,
                model.lang_code == lang,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def del_one_item_by_origin_elem_and_budg_id_by_lng_admin(
        db, budg_descr_id, budg_id, lang, model
    ):
        item = db.query(model).filter(
            model.is_deleted == bool(0),
            model.origin_elem_id == budg_descr_id,
            model.budget_id == budg_id,
            model.lang_code == lang,
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        item.update({"deleted_at": datetime.now(), "is_deleted": True})
        db.commit()

    @staticmethod
    def get_one_item_by_origin_elem_and_budg_id_by_lng_excless_adm(
        db, budg_descr_id, budg_id, lang, model
    ):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == budg_descr_id,
                model.budget_id == budg_id,
                model.lang_code == lang,
            )
            .first()
        )
        return item

    @staticmethod
    def get_one_item_by_origin_elem_id_and_by_lng_admin(
        db, origin_elem_id, lang, model
    ):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_orig_el_id_by_lng_excless_admin(
        db, origin_elem_id, lang, model
    ):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang,
            )
            .first()
        )
        return item

    @staticmethod
    def get_all_items_by_proj_id_by_lng_admin(db, proj_id, lang, model):
        items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.project_id == proj_id,
                model.lang_code == lang,
            )
            .order_by(desc(model.created_at))
            .all()
        )
        if items is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return items

    @staticmethod
    def get_all_items_by_proj_id_by_lng_clnt(db, proj_id, lang, model):
        items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.project_id == proj_id,
                model.lang_code == lang,
            )
            .order_by(desc(model.created_at))
            .all()
        )
        if items is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return items

    @staticmethod
    def get_one_item_by_origin_elem_and_proj_id_by_lng_admin(
        db, proj_id, origin_elem_id, lang, model
    ):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.project_id == proj_id,
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_orig_elem_and_proj_id_by_lng_for_upd_adm(
        db, proj_id, origin_elem_id, lang, model
    ):
        item = db.query(model).filter(
            model.is_deleted == bool(0),
            model.project_id == proj_id,
            model.origin_elem_id == origin_elem_id,
            model.lang_code == lang,
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def update_exists_item_by_orig_elem_and_proj_id_by_lng_admin(
        request, db, project_id, origin_elem_id, lang, model
    ):
        item = (
            DbQuery.get_one_item_by_orig_elem_and_proj_id_by_lng_for_upd_adm(
                db, project_id, origin_elem_id, lang, model
            )
        )
        if type(request) == dict:
            item.update(request)
        else:
            item.update(request.dict())
        db.commit()
        return item.first()

    @staticmethod
    def del_one_item_by_orig_elem_and_proj_id_by_lng_admin(
        db, proj_id, origin_elem_id, lang, model
    ):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.project_id == proj_id,
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        item.update({"deleted_at": datetime.now(), "is_deleted": True})
        db.commit()

    @staticmethod
    def get_one_item_by_origin_elem_id_and_id_admin(
        db, origin_elem_id, item_id, model
    ):
        items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
                model.id == item_id,
            )
            .first()
        )
        if items is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return items

    @staticmethod
    def get_one_item_by_origin_elem_id_admin(db, origin_elem_id, model):
        items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
            )
            .order_by(desc(model.created_at))
            .all()
        )
        if items is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return items

    @staticmethod
    def get_all_items_by_origin_elem_id_by_lng_admin(
        db, origin_elem_id, lang, model
    ):
        items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang,
            )
            .order_by(desc(model.created_at))
            .all()
        )
        if items is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return items

    @staticmethod
    def get_item_by_origin_elem_id_by_lng_admin(
        db, origin_elem_id, lang, model
    ):
        items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang,
            )
            .first()
        )
        if items is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return items

    @staticmethod
    def get_one_item_by_origin_elem_id_by_lng_admin(
        db, origin_elem_id, lang, model
    ):
        items = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.origin_elem_id == origin_elem_id,
                model.lang_code == lang,
            )
            .order_by(desc(model.created_at))
            .all()
        )
        if items is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return items

    @staticmethod
    def get_one_item_by_id_and_orig_elem_id_admin(
        db, origin_elem_id, item_id, model
    ):
        item = (
            db.query(model)
            .filter(
                model.is_deleted == bool(0),
                model.is_active == bool(1),
                model.origin_elem_id == origin_elem_id,
                model.id == item_id,
            )
            .first()
        )
        if item is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def get_one_item_by_id_and_orig_elem_id_for_upd_admin(
        db, origin_elem_id, item_id, model
    ):
        item = db.query(model).filter(
            model.is_deleted == bool(0),
            model.is_active == bool(1),
            model.origin_elem_id == origin_elem_id,
            model.id == item_id,
        )
        if item.first() is None:
            raise DbQuery.exception_404(model.__tablename__.capitalize())
        return item

    @staticmethod
    def upd_exists_by_id_and_orig_elem_id_for_adm(
        request, db, origin_elem_id, item_id, model
    ):

        item = DbQuery.get_one_item_by_id_and_orig_elem_id_for_upd_admin(
            db, origin_elem_id, item_id, model
        )
        if type(request) == dict:
            item.update(request)
        else:
            item.update(request.dict())
        db.commit()
        return item.first()

    @staticmethod
    def del_exists_by_id_and_orig_elem_id_for_adm(
        db, origin_elem_id, item_id, model
    ):

        item = DbQuery.get_one_item_by_id_and_orig_elem_id_for_upd_admin(
            db, origin_elem_id, item_id, model
        )
        item.update({"deleted_at": datetime.now(), "is_deleted": True})
        db.commit()
