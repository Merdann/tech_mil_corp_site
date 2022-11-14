import os
import shutil
from typing import Callable
from uuid import uuid4

from core.database.base.query_helpers import DbQuery
from core.database.models.languages import Language
from core.exceptions import exceptions
from PIL import Image


USERS = {
    "allowed_image_types": [
        "image/svg+xml",
        "image/jpeg",
        "image/png",
    ],
    "allowed_image_size": 5_000_000,
}

PROJECTS = {
    "allowed_mutlimedia_types": [
        "image/png",
        "image/jpeg",
        "video/mp4",
    ],
    "allowed_multimedia_size": [
        3_000_000,
        40_000_000,
    ],
}


MAIN_VIDEO = {
    "allowed_video_types": [
        "video/mp4",
    ],
    "allowed_video_size": 40_000_000,
}


def create_migrations_dirs():
    migrations = "migrations"
    versions_include = "versions"

    if not os.path.exists(f"{migrations}"):
        os.mkdir(f"{migrations}")

    if not os.path.exists(f"{migrations}/{versions_include}"):
        os.mkdir(f"{migrations}/{versions_include}")


def create_static_dirs():
    main_static = "static"
    static_include = ["images", "videos", "animations"]
    imgs_videos_animations = ["projects"]
    imgs = ["users"]
    videos = ["main_video"]

    if not os.path.exists(f"{main_static}"):
        os.mkdir(f"{main_static}")

    for dir in static_include:
        if not os.path.exists(f"{main_static}/{dir}"):
            os.mkdir(f"{main_static}/{dir}")

    for dir in imgs:
        if not os.path.exists(f"{main_static}/images/{dir}"):
            os.mkdir(f"{main_static}/images/{dir}")

    for dir in imgs_videos_animations:
        if not os.path.exists(f"{main_static}/images/{dir}"):
            os.mkdir(f"{main_static}/images/{dir}")
        if not os.path.exists(f"{main_static}/videos/{dir}"):
            os.mkdir(f"{main_static}/videos/{dir}")
        if not os.path.exists(f"{main_static}/animations/{dir}"):
            os.mkdir(f"{main_static}/animations/{dir}")

    for dir in videos:
        if not os.path.exists(f"{main_static}/videos/{dir}"):
            os.mkdir(f"{main_static}/videos/{dir}")


def default_images_for_fixtures_dir_name() -> str:
    """
    Return "core/database/base" directory name.
    """
    images_for_fixtures_dir = "core/database/base"
    return images_for_fixtures_dir


def static_users_dir_name() -> str:
    """
    Return "static/images/users" directory name.
    """
    users_dir = "static/images/users"
    return users_dir


def static_projects_video_dir_name() -> str:
    """
    Return "static/videos/projects" directory name.
    """
    projects_dir = "static/videos/projects"
    return projects_dir


def static_projects_image_dir_name() -> str:
    """
    Return "static/images/projects" directory name.
    """
    projects_dir = "static/images/projects"
    return projects_dir


def static_projects_animation_dir_name() -> str:
    """
    Return "static/animations/projects" directory name.
    """
    projects_dir = "static/animations/projects"
    return projects_dir


def static_main_video_videos_dir_name() -> str:
    """
    Return "static/videos/main_video" directory name.
    """
    main_video_dir = "static/videos/main_video"
    return main_video_dir


def personal_dirname(title: str) -> str:
    """
    Return dirname based on title with replaced
    whitespace to underscore.
    """
    personal_dirname = "_".join(title.strip().lower().split())
    if "/" in personal_dirname:
        personal_dirname = personal_dirname.replace("/", "_")
    return personal_dirname


def personal_dir_path_for_save(
    title: str, parrent_dir_name_func: Callable
) -> str:
    """
    Create if not exists presonal directory based on title
    inside parrent_di_name_func folder and return that path name.
    """
    new_title = personal_dirname(title)
    path = f"{parrent_dir_name_func}/{new_title}"
    if not os.path.exists(path):
        os.mkdir(f"{parrent_dir_name_func}/{new_title}")
    return path


def renamed_file_name(file_name: str) -> str:
    """
    Return filename based on file_name with replaced
    whitespace to underscore and added in the end of file
    string with uuid4 type.
    """
    file_name = file_name.replace(" ", "_")
    new_fn = []
    for symbol in file_name:
        if symbol == "(" or symbol == ")":
            symbol = "_"
        new_fn.append(symbol)
    file_name = "".join(new_fn)
    file_ext = file_name.split(".")[-1]
    ind_of_ext = file_name.find(file_ext) - 1
    without_ext = file_name[:ind_of_ext]
    uniq_str = str(uuid4())
    new_without_ext = f"{without_ext}-{uniq_str}"
    new_file_name = f"{new_without_ext}.{file_ext}"
    return new_file_name


def dir_with_file_for_save_path(
    title: str, static_dir_name_func_for_save: Callable, filename_for_save: str
) -> str:
    """
    Return file path with for save in the db table field.
    """
    path_dir = personal_dir_path_for_save(title, static_dir_name_func_for_save)
    renamed_file = renamed_file_name(filename_for_save)
    return f"{path_dir}/{renamed_file}"


def save_uploaded_file_and_return_file_path(
    title: str,
    static_dir_name_func_for_save: Callable,
    filename_for_save: str,
    fileobj_for_save: object,
) -> str:
    """
    Create if not exists presonal directory based on title
    inside static_dir_name_func_for_save folder.
    Replace whitespace to underscore in filename_for_save
    and add in the end of file string with uuid4 type
    for add in the end of path for save.
    Save fileobj_for_save to static_dir_name_func_for_save.
    Return file path for save in the db table field.
    """
    title = "_".join(str(title).strip().lower().split())
    if "/" in title:
        title = title.replace("/", "_-_")
    dir_file_for_save = dir_with_file_for_save_path(
        title, static_dir_name_func_for_save, filename_for_save
    )
    with open(dir_file_for_save, "w+b") as buffer:
        shutil.copyfileobj(fileobj_for_save, buffer)

    return dir_file_for_save


def get_lowercase_title(title: str):
    title = title.lower()
    return title


def get_capitalize_title(title: str):
    title = title.capitalize()
    return title


def get_titleize_title(title: str):
    title = title.title()
    return title


def replace_and_save_img_to_thumbnail(image: str):
    img = Image.open(image)
    img.thumbnail(size=(176, 176))
    img.save(image)
    return img


def data_with_deleted_empty_fields(all_data, is_active):
    data = {}
    for k, v in all_data.items():
        if v:
            data[k] = v
    if is_active is False:
        data["is_active"] = False
    else:
        data["is_active"] = True
    return data


def exception_if_language_does_not_exists(db, lang_code):
    language_exists = DbQuery.get_one_item_by_code_exceptionless_admin(
        db, lang_code, Language
    )
    if not language_exists:
        raise exceptions.exception_not_found("Language")
