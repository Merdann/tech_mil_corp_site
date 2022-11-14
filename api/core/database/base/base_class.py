from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr


@as_declarative()
class Base:

    __name__: str

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
