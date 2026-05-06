import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class MediaType(enum.Enum):
    movie = "movie"
    book = "book"
    game = "game"

class MediaItem(Base):
    __tablename__ = "media_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType))
    creator: Mapped[str] = mapped_column(String(255), nullable=True)

    added_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    added_by_user = relationship("User", back_populates="media_items")

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    ratings = relationship("MediaRating", back_populates="media_item", cascade="all, delete-orphan")


Index("ix_media_items_type_title", MediaItem.media_type, MediaItem.title)


