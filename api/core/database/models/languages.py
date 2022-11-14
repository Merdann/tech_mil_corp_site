from core.database.base.base_class import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Language(Base):
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)

    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    user = relationship("User", back_populates="languages")

    projects = relationship("Project", back_populates="origin_lang")
    project_translations = relationship(
        "ProjectTranslation", back_populates="language"
    )

    def __repr__(self) -> str:
        return f"{self.name}"
