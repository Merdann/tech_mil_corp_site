from core.database.base.base_class import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Project(Base):
    title_highlight = Column(String, nullable=False)
    title_head = Column(String, nullable=False)
    description = Column(String, nullable=False)
    multimedia = Column(String, nullable=False)

    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    origin_lang_code = Column(
        String, ForeignKey("language.code"), nullable=False
    )

    user = relationship("User", back_populates="projects")
    origin_lang = relationship("Language", back_populates="projects")

    project_images = relationship("ProjectImage", back_populates="project")
    project_videos = relationship("ProjectVideo", back_populates="project")
    project_translations = relationship(
        "ProjectTranslation", back_populates="project"
    )

    def __repr__(self) -> str:
        return f"{self.id}"


class ProjectImage(Base):
    image = Column(String, nullable=False)

    origin_elem_id = Column(
        UUID(as_uuid=True), ForeignKey("project.id"), nullable=False
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    user = relationship("User", back_populates="project_images")
    project = relationship("Project", back_populates="project_images")

    def __repr__(self) -> str:
        return f"{self.id}"


class ProjectVideo(Base):
    video = Column(String, nullable=False)

    origin_elem_id = Column(
        UUID(as_uuid=True), ForeignKey("project.id"), nullable=False
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    user = relationship("User", back_populates="project_videos")
    project = relationship("Project", back_populates="project_videos")

    def __repr__(self) -> str:
        return f"{self.id}"


class ProjectTranslation(Base):
    title_highlight = Column(String, nullable=False)
    title_head = Column(String, nullable=False)
    description = Column(String, nullable=False)
    lang_code = Column(String, ForeignKey("language.code"), nullable=False)

    origin_elem_id = Column(
        UUID(as_uuid=True), ForeignKey("project.id"), nullable=False
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    language = relationship("Language", back_populates="project_translations")

    user = relationship("User", back_populates="project_translations")
    project = relationship("Project", back_populates="project_translations")

    def __repr__(self) -> str:
        return f"{self.id}"
