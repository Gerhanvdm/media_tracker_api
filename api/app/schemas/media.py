from datetime import datetime

from pydantic import BaseModel, Field

from app.models.media import MediaType

class MediaCreate(BaseModel):
    tite: str = Field(min_length=3, max_length=255)
    media_type: MediaType
    creator: str | None = Field(default=None, min_length=3, max_length=255)
    added_by_user_id: int

class MediaUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    media_type: MediaType | None = None
    creator: str | None = Field(default=None, min_length=3, max_length=255)

class MediaRead(BaseModel):
    id : int
    title: str
    media_type: MediaType
    creator: str | None
    added_by_user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

    
