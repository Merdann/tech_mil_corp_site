from core.additional_helpers import default_images_for_fixtures_dir_name
from core.additional_helpers import dir_with_file_for_save_path
from core.additional_helpers import static_users_dir_name
from core.config import settings
from core.database.base.session import SessionLocal
from core.database.models.languages import Language
from core.database.models.users import User
from core.security import Password
from PIL import Image


def create_superuser():
    db = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.username == settings.SUPERUSER_USERNAME,
            User.is_active == bool(1),
            User.is_deleted == bool(0),
            User.is_superuser == bool(1),
        )
        .first()
    )
    if not user:
        file_name_usr = "default_user_avatar.png"
        file_supusr = (
            f"{default_images_for_fixtures_dir_name()}/{file_name_usr}"
        )
        super_file_path_to_save = dir_with_file_for_save_path(
            settings.SUPERUSER_USERNAME,
            static_users_dir_name(),
            file_name_usr,
        )
        imgsupusr = Image.open(file_supusr)
        imgsupusr.save(super_file_path_to_save)
        imgsupusr.close()

        superuser = User(
            username=settings.SUPERUSER_USERNAME,
            hashed_password=Password.hashing_password(
                settings.SUPERUSER_PASSWORD
            ),
            avatar=super_file_path_to_save,
            is_superuser=True,
        )
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        return superuser
    return user


def create_basic_languages():
    db = SessionLocal()
    super_user = create_superuser()
    en = Language(name="English", code="en", owner_id=super_user.id)
    tm = Language(name="Turkmen", code="tm", owner_id=super_user.id)
    en_exists = db.query(Language).filter(Language.code == en.code).first()
    tm_exists = db.query(Language).filter(Language.code == tm.code).first()

    if not en_exists:
        db.add(en)
        db.commit()
    if not tm_exists:
        db.add(tm)
        db.commit()
