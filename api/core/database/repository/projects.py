from typing import List
from uuid import UUID

from core.additional_helpers import data_with_deleted_empty_fields
from core.additional_helpers import exception_if_language_does_not_exists
from core.additional_helpers import PROJECTS
from core.additional_helpers import save_uploaded_file_and_return_file_path
from core.additional_helpers import static_projects_image_dir_name
from core.additional_helpers import static_projects_video_dir_name
from core.database.base.query_helpers import DbQuery
from core.database.models.projects import Project
from core.database.models.projects import ProjectImage
from core.database.models.projects import ProjectTranslation
from core.database.models.projects import ProjectVideo
from core.database.models.users import User
from core.database.repository.languages import default_lang
from core.exceptions import exceptions
from core.security import FieldsValidations
from core.security import Tkn
from fastapi import Request
from fastapi import UploadFile
from sqlalchemy.orm.session import Session


def exception_if_project_exists(
    db: Session, title_highlight: str
):
    project_exists = (
        db.query(Project)
        .filter(
            Project.is_deleted == bool(0),
            Project.title_highlight == title_highlight,
            Project.origin_lang_code == default_lang(),
        )
        .first()
    )
    if project_exists:
        raise exceptions.exception_already_exists("Project")


def prepare_multimedia_for_save(
    multimedia: UploadFile,
    title_highlight: str,
):
    title = title_highlight
    multimedia_for_save = save_uploaded_file_and_return_file_path(
        title,
        static_projects_image_dir_name(),
        multimedia.filename,
        multimedia.file,
    )
    return multimedia_for_save


def prepare_project_images_for_save(project_images: list, title: str):
    prj_imgs_for_save = []
    if project_images:
        for prj_img in project_images:
            prj_img_for_save = save_uploaded_file_and_return_file_path(
                title,
                static_projects_image_dir_name(),
                prj_img.filename,
                prj_img.file,
            )
            prj_imgs_for_save.append(prj_img_for_save)
    return prj_imgs_for_save


def prepare_project_videos_for_save(project_videos: list, title: str):
    prj_videos_for_save = []
    if project_videos:
        for prj_video in project_videos:
            prj_video_for_save = save_uploaded_file_and_return_file_path(
                title,
                static_projects_video_dir_name(),
                prj_video.filename,
                prj_video.file,
            )
            prj_videos_for_save.append(prj_video_for_save)
    return prj_videos_for_save


def check_origin_elem_and_project_exists(origin_elem_id: UUID, db: Session):
    if not origin_elem_id:
        raise exceptions.exception_something_went_wrong()
    project_exists = DbQuery.get_one_item_by_id_admin(
        db, origin_elem_id, Project
    )
    if not project_exists:
        raise exceptions.exception_not_found("Project")


def exception_if_project_translation_exists(
    db: Session, lang_code: str, origin_elem_id: UUID
):
    project_translation_exists = (
        db.query(ProjectTranslation)
        .filter(
            ProjectTranslation.is_deleted == bool(0),
            ProjectTranslation.lang_code == lang_code,
            ProjectTranslation.origin_elem_id == origin_elem_id,
        )
        .first()
    )
    if project_translation_exists:
        raise exceptions.exception_already_exists("ProjectTranslation")


async def total_file_sizes_and_counts(
    multimedia, project_images, project_videos
):
    total_file_sizes = 0
    multimedia_file_size = 0
    images_file_size = 0
    images_len = 0
    videos_file_size = 0
    videos_len = 0

    if multimedia:
        file_size = await multimedia.read()
        multimedia_file_size += len(file_size)
    if project_images:
        for image in project_images:
            file_size = await image.read()
            total_file_sizes += len(file_size)
            images_file_size += len(file_size)
            images_len += 1
    if project_videos:
        for video in project_images:
            file_size = await video.read()
            total_file_sizes += len(file_size)
            videos_file_size += len(file_size)
            videos_len += 1
    return {
        "total_file_sizes": total_file_sizes,
        "multimedia_file_size": multimedia_file_size,
        "images_file_size": images_file_size,
        "images_len": images_len,
        "videos_file_size": videos_file_size,
        "videos_len": videos_len,
    }


async def check_files_sizes(
    multimedia,
    project_images,
    project_videos,
):
    total_files_info = await total_file_sizes_and_counts(
        multimedia,
        project_images,
        project_videos,
    )

    multimedia_file_size = total_files_info["multimedia_file_size"]
    images_file_size = total_files_info["images_file_size"]
    images_len = total_files_info["images_len"]
    videos_file_size = total_files_info["videos_file_size"]
    videos_len = total_files_info["videos_len"]

    if multimedia:
        allowed_multimedia_size = PROJECTS.get("allowed_multimedia_size")[:1]
        if project_images and project_videos:
            allowed_images_size = (
                PROJECTS.get("allowed_multimedia_size")[0] * images_len
            )
            allowed_videos_size = (
                PROJECTS.get("allowed_multimedia_size")[-1] * videos_len
            )
            total_uploaded_size = (
                multimedia_file_size + images_file_size + videos_file_size
            )
            total_allowed_size = (
                allowed_multimedia_size
                + allowed_images_size
                + allowed_videos_size
            )

            exceptions.exception_by_compare_file_size(
                total_uploaded_size, total_allowed_size
            )
        elif project_images:
            allowed_images_size = (
                PROJECTS.get("allowed_multimedia_size")[:1] * images_len
            )
            total_uploaded_size = multimedia_file_size + images_file_size
            total_allowed_size = allowed_multimedia_size + allowed_images_size

            exceptions.exception_by_compare_file_size(
                total_uploaded_size, total_allowed_size
            )
        elif project_videos:
            allowed_videos_size = (
                PROJECTS.get("allowed_multimedia_size")[-1] * videos_len
            )
            total_uploaded_size = multimedia_file_size + videos_file_size
            total_allowed_size = allowed_multimedia_size + allowed_videos_size

            exceptions.exception_by_compare_file_size(
                total_uploaded_size, total_allowed_size
            )

        else:
            exceptions.exception_by_compare_file_size(
                multimedia_file_size, allowed_multimedia_size
            )


def check_files_types(
    multimedia=None,
    project_images=None,
    project_videos=None,
):
    if multimedia:
        exceptions.exception_by_checking_file_types(
            multimedia, PROJECTS.get("allowed_mutlimedia_types")[:2]
        )
    if project_images:
        for image in project_images:
            exceptions.exception_by_checking_file_types(
                image, PROJECTS.get("allowed_mutlimedia_types")[:2]
            )
    if project_videos:
        for video in project_videos:
            exceptions.exception_by_checking_file_types(
                video, PROJECTS.get("allowed_mutlimedia_types")[2:]
            )


def display_only_not_deleted_images(project):
    all_imgs = project.project.project_images
    if all_imgs:
        imgs = [img for img in all_imgs if img.is_deleted is False]
        project.project.project_images = imgs


def display_only_not_deleted_videos(project):
    all_videos = project.project.project_videos
    if all_videos:
        vds = [vd for vd in all_videos if vd.is_deleted is False]
        project.project.project_videos = vds


def get_all_projects_client(lang: str, db: Session):
    all_projects = DbQuery.get_all_items_by_lang_client(
        db, lang, ProjectTranslation
    )
    return all_projects


def get_one_project_client(project_id: UUID, lang: str, db: Session):
    project = DbQuery.get_one_item_by_lang_id_client(
        db, project_id, lang, ProjectTranslation
    )

    display_only_not_deleted_images(project)
    display_only_not_deleted_videos(project)

    return project


async def create_project_translation(
    req: Request,
    title_highlight: str,
    description: str,
    origin_elem_id: UUID,
    lang_code: str,
    multimedia: UploadFile,
    project_images: List[UploadFile],
    project_videos: List[UploadFile],
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    exception_if_language_does_not_exists(db, lang_code)

    user_id = Tkn.user_id(tkn, User, db)

    if lang_code == default_lang():
        exception_if_project_exists(db, title_highlight)
        exceptions.exception_field_is_required(multimedia, "multimedia")

        check_files_types(multimedia, project_images, project_videos)
        check_files_sizes(multimedia, project_images, project_videos)

        multimedia_for_save = prepare_multimedia_for_save(
            multimedia,
            title_highlight,
        )

        project = Project(
            owner_id=user_id,
            title_highlight=title_highlight,
            description=description,
            multimedia=multimedia_for_save,
            origin_lang_code=lang_code,
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        project_translation = ProjectTranslation(
            owner_id=user_id,
            title_highlight=title_highlight,
            description=description,
            origin_elem_id=project.id,
            lang_code=lang_code,
        )
        db.add(project_translation)
        db.commit()
        db.refresh(project_translation)

        if project_images:
            prj_imgs_for_save = prepare_project_images_for_save(
                project_images, title_highlight
            )

            for prj_img in prj_imgs_for_save:
                pr_im = ProjectImage(
                    owner_id=user_id,
                    origin_elem_id=project.id,
                    image=prj_img,
                )
                db.add(pr_im)
            db.commit()

        if project_videos:
            prj_videos_for_save = prepare_project_videos_for_save(
                project_videos, title_highlight
            )

            for prj_video in prj_videos_for_save:
                pr_vid = ProjectVideo(
                    owner_id=user_id,
                    origin_elem_id=project.id,
                    video=prj_video,
                )
                db.add(pr_vid)
            db.commit()

    elif lang_code != default_lang():
        check_origin_elem_and_project_exists(origin_elem_id, db)
        exception_if_project_translation_exists(db, lang_code, origin_elem_id)

        project_translation = ProjectTranslation(
            owner_id=user_id,
            title_highlight=title_highlight,
            description=description,
            origin_elem_id=origin_elem_id,
            lang_code=lang_code,
        )

        db.add(project_translation)
        db.commit()
        db.refresh(project_translation)

    else:
        raise exceptions.exception_something_went_wrong()

    display_only_not_deleted_images(project_translation)
    display_only_not_deleted_videos(project_translation)

    return project_translation


def get_all_projects_admin(db: Session, tkn: str):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    all_projects = DbQuery.get_all_items_admin(db, Project)
    return all_projects


def get_one_project_admin(project_id: UUID, lang: str, tkn: str, db: Session):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    project = DbQuery.get_one_item_by_lang_id_admin(
        db, project_id, lang, ProjectTranslation
    )

    display_only_not_deleted_images(project)
    display_only_not_deleted_videos(project)

    return project


async def update_project_admin(
    req: Request,
    project_id: UUID,
    title_highlight: str,
    description: str,
    lang_code: str,
    multimedia: UploadFile,
    is_active: bool,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    mutlimedia_types = PROJECTS.get("allowed_mutlimedia_types")[:2]
    multimedia_size = PROJECTS.get("allowed_multimedia_size")[0]

    data = data_with_deleted_empty_fields(
        {
            "title_highlight": title_highlight,
            "description": description,
            "is_active": is_active,
        },
        is_active,
    )

    if lang_code == default_lang():
        project_origin = DbQuery.get_one_item_by_id_admin(
            db, project_id, Project
        )
        if title_highlight:
            project_origin.title_highlight = title_highlight
        if description:
            project_origin.description = description

        if multimedia:
            if not FieldsValidations.correct_file_size(req, multimedia_size):
                raise exceptions.exception_uploading_file_to_large(
                    multimedia_size
                )
            if multimedia.content_type not in mutlimedia_types:
                raise exceptions.exception_incorrect_content_type(
                    mutlimedia_types, "multimedia"
                )
            multimedia_for_save = prepare_multimedia_for_save(
                multimedia,
                project_origin.title_highlight,
            )
            project_origin.multimedia = multimedia_for_save
        db.commit()

    project = DbQuery.update_exists_item_by_lang_id_admin(
        data, db, project_id, lang_code, ProjectTranslation
    )

    display_only_not_deleted_images(project)
    display_only_not_deleted_videos(project)

    return project


def add_project_images_admin(
    req: Request,
    project_id: UUID,
    default_language: str,
    project_images: List[UploadFile],
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    if project_images:
        image_types = PROJECTS.get("allowed_mutlimedia_types")[1:3]
        multimedia_size = PROJECTS.get("allowed_multimedia_size")[0]

        if not FieldsValidations.correct_file_size(req, multimedia_size):
            raise exceptions.exception_uploading_file_to_large(multimedia_size)
        for project_image in project_images:
            if project_image.content_type not in image_types:
                raise exceptions.exception_incorrect_content_type(
                    image_types, "project_image"
                )

        project_origin = DbQuery.get_one_item_by_id_admin(
            db, project_id, Project
        )
        prj_imgs_for_save = prepare_project_images_for_save(
            project_images, project_origin.title_highlight
        )

        user_id = Tkn.user_id(tkn, User, db)
        for prj_img in prj_imgs_for_save:
            pr_im = ProjectImage(
                owner_id=user_id,
                origin_elem_id=project_origin.id,
                image=prj_img,
            )
            db.add(pr_im)
        db.commit()

    project = DbQuery.get_one_item_by_lang_id_admin(
        db, project_id, default_lang(), ProjectTranslation
    )

    display_only_not_deleted_images(project)
    display_only_not_deleted_videos(project)

    return project


def update_project_image_admin(
    req: Request,
    project_id: UUID,
    project_image_id: UUID,
    new_project_image: UploadFile,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    image_types = PROJECTS.get("allowed_mutlimedia_types")[:2]
    multimedia_size = PROJECTS.get("allowed_multimedia_size")[0]

    if not FieldsValidations.correct_file_size(req, multimedia_size):
        raise exceptions.exception_uploading_file_to_large(multimedia_size)
    if new_project_image.content_type not in image_types:
        raise exceptions.exception_incorrect_content_type(
            image_types, "project_image"
        )

    project_origin = DbQuery.get_one_item_by_id_admin(db, project_id, Project)
    prj_imgs_for_save = prepare_project_images_for_save(
        [new_project_image], project_origin.title_highlight
    )

    proj_image = DbQuery.get_one_item_by_id_admin(
        db, project_image_id, ProjectImage
    )
    proj_image.image = prj_imgs_for_save[0]
    db.commit()

    project = DbQuery.get_one_item_by_lang_id_admin(
        db, project_id, default_lang(), ProjectTranslation
    )

    display_only_not_deleted_images(project)
    display_only_not_deleted_videos(project)

    return project


def delete_project_image_admin(
    project_id: UUID,
    project_image_id: UUID,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    DbQuery.del_exists_by_id_and_orig_elem_id_for_adm(
        db, project_id, project_image_id, ProjectImage
    )


async def add_project_videos_admin(
    req: Request,
    project_id: UUID,
    default_language: str,
    project_videos: List[UploadFile],
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    if project_videos:
        video_types = PROJECTS.get("allowed_mutlimedia_types")[2:]
        video_size = PROJECTS.get("allowed_multimedia_size")[-1]

        if not FieldsValidations.correct_file_size(req, video_size):
            raise exceptions.exception_uploading_file_to_large(video_size)
        for project_video in project_videos:
            if project_video.content_type not in video_types:
                raise exceptions.exception_incorrect_content_type(
                    video_types, "project_image"
                )

        project_origin = DbQuery.get_one_item_by_id_admin(
            db, project_id, Project
        )
        prj_videos_for_save = prepare_project_images_for_save(
            project_videos, project_origin.title_highlight
        )

        user_id = Tkn.user_id(tkn, User, db)
        for prj_vid in prj_videos_for_save:
            pr_v = ProjectVideo(
                owner_id=user_id,
                origin_elem_id=project_origin.id,
                video=prj_vid,
            )
            db.add(pr_v)
        db.commit()

    project = DbQuery.get_one_item_by_lang_id_admin(
        db, project_id, default_lang(), ProjectTranslation
    )

    display_only_not_deleted_images(project)
    display_only_not_deleted_videos(project)

    return project


def update_project_video_admin(
    req: Request,
    project_id: UUID,
    project_video_id: UUID,
    new_project_video: UploadFile,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)

    video_types = PROJECTS.get("allowed_mutlimedia_types")[2:]
    video_size = PROJECTS.get("allowed_multimedia_size")[-1]

    if not FieldsValidations.correct_file_size(req, video_size):
        raise exceptions.exception_uploading_file_to_large(video_size)
    if new_project_video.content_type not in video_types:
        raise exceptions.exception_incorrect_content_type(
            video_types, "project_video"
        )

    project_origin = DbQuery.get_one_item_by_id_admin(db, project_id, Project)
    prj_videos_for_save = prepare_project_videos_for_save(
        [new_project_video], project_origin.title_highlight
    )

    proj_video = DbQuery.get_one_item_by_id_admin(
        db, project_video_id, ProjectVideo
    )
    proj_video.video = prj_videos_for_save[0]
    db.commit()

    project = DbQuery.get_one_item_by_lang_id_admin(
        db, project_id, default_lang(), ProjectTranslation
    )

    display_only_not_deleted_images(project)
    display_only_not_deleted_videos(project)

    return project


def delete_project_video_admin(
    project_id: UUID,
    project_video_id: UUID,
    tkn: str,
    db: Session,
):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    DbQuery.del_exists_by_id_and_orig_elem_id_for_adm(
        db, project_id, project_video_id, ProjectVideo
    )


def delete_project_admin(project_id: UUID, db: Session, tkn: str):
    Tkn.is_access_tkn_and_active_user_or_exc(tkn, db)
    DbQuery.delete_one_item_by_id_admin(db, project_id, Project)
    DbQuery.delete_all_images_by_origin_elem_id_admin(
        db, project_id, ProjectImage
    )
    DbQuery.delete_all_translated_items_by_item_id_admin(
        db, project_id, ProjectTranslation
    )
