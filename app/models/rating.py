from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MediaRating(Base):
    __tablename__ = "media_ratings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    media_id: Mapped[int] = mapped_column(
        ForeignKey("media_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    media_item = relationship("MediaItem", back_populates="ratings")
    user = relationship("User", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("media_id", "user_id", name="uq_media_rating_media_user"),
        CheckConstraint("rating >= 1 AND rating <= 10", name="ck_rating_between_1_and_10"),
        Index("ix_media_ratings_media_user", "media_id", "user_id"),
    )


