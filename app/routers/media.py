from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.media import MediaItem, MediaType
from app.models.user import User
from app.schemas.media import MediaCreate, MediaRead, MediaUpdate

router = APIRouter(prefix="/media", tags=["Media"])


@router.post("/", response_model=MediaRead, status_code=status.HTTP_201_CREATED)
async def create_media(payload: MediaCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, payload.added_by_user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    media = MediaItem(
        title=payload.title,
        media_type=payload.media_type,
        creator=payload.creator,
        added_by_user_id=payload.added_by_user_id,
    )

    db.add(media)
    await db.commit()
    await db.refresh(media)

    return media


@router.get("/", response_model=list[MediaRead])
async def list_media(
    media_type: MediaType | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(MediaItem).order_by(MediaItem.id)

    if media_type is not None:
        stmt = stmt.where(MediaItem.media_type == media_type)

    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{media_id}", response_model=MediaRead)
async def get_media(media_id: int, db: AsyncSession = Depends(get_db)):
    media = await db.get(MediaItem, media_id)

    if media is None:
        raise HTTPException(status_code=404, detail="Media item not found")

    return media


@router.patch("/{media_id}", response_model=MediaRead)
async def update_media(
    media_id: int,
    payload: MediaUpdate,
    db: AsyncSession = Depends(get_db),
):
    media = await db.get(MediaItem, media_id)

    if media is None:
        raise HTTPException(status_code=404, detail="Media item not found")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(media, field, value)

    await db.commit()
    await db.refresh(media)

    return media


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(media_id: int, db: AsyncSession = Depends(get_db)):
    media = await db.get(MediaItem, media_id)

    if media is None:
        raise HTTPException(status_code=404, detail="Media item not found")

    await db.delete(media)
    await db.commit()

    return None