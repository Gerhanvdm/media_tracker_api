from datetime import datetime

from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    user_id: int
    rating: int = Field(ge=1, le=10)
    comment: str | None = None


class RatingUpdate(BaseModel):
    user_id: int
    rating: int | None = Field(default=None, ge=1, le=10)
    comment: str | None = None


class RatingRead(BaseModel):
    id: int
    media_id: int
    user_id: int
    rating: int
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}