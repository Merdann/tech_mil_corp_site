from uuid import UUID

from core.database.base.query_helpers import DbQuery
from core.database.models.follow_us import FollowUs
from core.exceptions import exceptions
from core.security import FieldsValidations
from core.security import Tkn
from pydantic import EmailStr
from sqlalchemy.orm.session import Session


async def post_info_with_email(
    email: EmailStr,
    db: Session,
):
    if not FieldsValidations.correct_email(email):
        raise exceptions.exception_incorrect_email()
    exists = DbQuery.get_one_item_by_email_admin_exceptionless(
        db, email, FollowUs
    )
    if not exists:
        await DbQuery.create_element(
            db=db, tkn=None, model=FollowUs, data={"email": email}
        )
    return {"detail": "OK"}


async def get_all_followed_emails_admin(
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    items = DbQuery.get_all_items_admin(db, FollowUs)
    return items


def delete_follower_admin(follower_id: UUID, tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    DbQuery.delete_one_item_by_id_admin(db, follower_id, FollowUs)
