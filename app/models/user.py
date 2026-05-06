from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    media_items = relationship("MediaItem", back_populates="added_by_user")
    ratings = relationship("MediaRating", back_populates="user", cascade="all, delete-orphan")


