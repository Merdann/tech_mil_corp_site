from core.database.base.base_class import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class CarouselAbout(Base):
    image = Column(String, nullable=True)

    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    user = relationship("User", back_populates="carousels_about")

    def __repr__(self) -> str:
        return f"{self.id}"
