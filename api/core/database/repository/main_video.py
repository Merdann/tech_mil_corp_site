from uuid import UUID

from core.additional_helpers import MAIN_VIDEO
from core.additional_helpers import save_uploaded_file_and_return_file_path
from core.additional_helpers import static_main_video_videos_dir_name
from core.database.base.query_helpers import DbQuery
from core.database.models.main_video import MainVideo
from core.database.models.users import User
from core.exceptions import exceptions
from core.security import FieldsValidations
from core.security import Tkn
from fastapi import Request
from fastapi import UploadFile
from sqlalchemy.orm.session import Session


def prepare_main_video_for_save(
    main_video: UploadFile,
    user_name: str,
):
    main_video_for_save = save_uploaded_file_and_return_file_path(
        user_name,
        static_main_video_videos_dir_name(),
        main_video.filename,
        main_video.file,
    )
    return main_video_for_save


def get_main_video_client(db: Session):
    main_video = DbQuery.get_all_items_client(db, MainVideo)
    return main_video


def create_main_video(
    req: Request,
    video: UploadFile,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    video_types = MAIN_VIDEO.get("allowed_video_types")
    video_size = MAIN_VIDEO.get("allowed_video_size")

    if not FieldsValidations.correct_file_size(req, video_size):
        raise exceptions.exception_uploading_file_to_large(video_size)

    if video.content_type not in video_types:
        raise exceptions.exception_incorrect_content_type(video_types, "video")

    user_id = Tkn.user_id(tkn, User, db)
    user_name = DbQuery.get_one_active_user_by_user_id(db, user_id, User)

    main_video_for_save = prepare_main_video_for_save(video, user_name)

    main_video = MainVideo(
        owner_id=user_id,
        video=main_video_for_save,
    )
    db.add(main_video)
    db.commit()
    db.refresh(main_video)

    return main_video


def get_main_video_admin(tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    main_video = DbQuery.get_all_items_admin(db, MainVideo)
    return main_video


def get_one_video_admin(video_id: UUID, tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    video = DbQuery.get_one_item_by_id_admin(db, video_id, MainVideo)
    return video


def update_video_admin(
    video_id: UUID,
    req: Request,
    video: UploadFile,
    is_active: bool,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    video_exists = DbQuery.get_one_item_by_id_admin(db, video_id, MainVideo)

    if video:
        video_types = MAIN_VIDEO.get("allowed_video_types")
        video_size = MAIN_VIDEO.get("allowed_video_size")

        if not FieldsValidations.correct_file_size(req, video_size):
            raise exceptions.exception_uploading_file_to_large(video_size)

        if video.content_type not in video_types:
            raise exceptions.exception_incorrect_content_type(
                video_types, "video"
            )

        user_id = Tkn.user_id(tkn, User, db)
        user_name = DbQuery.get_one_active_user_by_user_id(db, user_id, User)

        main_video_for_save = prepare_main_video_for_save(video, user_name)

        video_exists.video = main_video_for_save

    video_exists.is_active = is_active

    db.commit()
    db.refresh(video_exists)

    return video_exists


def delete_video_admin(video_id: UUID, tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    DbQuery.delete_one_item_by_id_admin(db, video_id, MainVideo)
