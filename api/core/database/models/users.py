from datetime import datetime

from core.database.base.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    username = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    languages = relationship("Language", back_populates="user")

    blacklisted_jwts = relationship("BlacklistedJWTS", back_populates="user")
    projects = relationship("Project", back_populates="user")
    project_images = relationship("ProjectImage", back_populates="user")
    project_videos = relationship("ProjectVideo", back_populates="user")
    project_translations = relationship(
        "ProjectTranslation", back_populates="user"
    )
    videos = relationship("MainVideo", back_populates="user")
    carousels_main = relationship("CarouselMain", back_populates="user")

    def __repr__(self) -> str:
        return f"{self.username}"


class BlacklistedJWTS(Base):
    jwt = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    jwt_created = Column(DateTime, nullable=False)
    jwt_expires = Column(DateTime, nullable=False)
    jwt_blacklisted = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="blacklisted_jwts")

    def __repr__(self) -> str:
        return f"{self.jwt}"
