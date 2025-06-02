from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import DateTime, String, func
import uuid
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class SharedColumnsMixin:
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    created_by: Mapped[str] = mapped_column(String, nullable=True)
    updated_by: Mapped[str] = mapped_column(String, nullable=True)
