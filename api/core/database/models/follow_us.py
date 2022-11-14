from core.database.base.base_class import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class FollowUs(Base):
    email = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}"
