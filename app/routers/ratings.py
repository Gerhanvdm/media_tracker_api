from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.media import MediaItem
from app.models.rating import MediaRating
from app.models.user import User
from app.schemas.rating import RatingCreate, RatingRead, RatingUpdate

router = APIRouter(tags=["Ratings"])


@router.post(
    "/media/{media_id}/ratings",
    response_model=RatingRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_rating(
    media_id: int,
    payload: RatingCreate,
    db: AsyncSession = Depends(get_db),
):
    media = await db.get(MediaItem, media_id)

    if media is None:
        raise HTTPException(status_code=404, detail="Media item not found")

    user = await db.get(User, payload.user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    rating = MediaRating(
        media_id=media_id,
        user_id=payload.user_id,
        rating=payload.rating,
        comment=payload.comment,
    )

    db.add(rating)

    try:
        await db.commit()
        await db.refresh(rating)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has already rated this media item",
        )

    return rating


@router.get("/media/{media_id}/ratings", response_model=list[RatingRead])
async def list_ratings_for_media(
    media_id: int,
    db: AsyncSession = Depends(get_db),
):
    media = await db.get(MediaItem, media_id)

    if media is None:
        raise HTTPException(status_code=404, detail="Media item not found")

    result = await db.execute(
        select(MediaRating)
        .where(MediaRating.media_id == media_id)
        .order_by(MediaRating.id)
    )

    return result.scalars().all()


@router.patch("/ratings/{rating_id}", response_model=RatingRead)
async def update_rating(
    rating_id: int,
    payload: RatingUpdate,
    db: AsyncSession = Depends(get_db),
):
    rating = await db.get(MediaRating, rating_id)

    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    if rating.user_id != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the user who created this rating can update it",
        )

    update_data = payload.model_dump(exclude_unset=True)
    update_data.pop("user_id", None)

    for field, value in update_data.items():
        setattr(rating, field, value)

    await db.commit()
    await db.refresh(rating)

    return rating


@router.delete("/ratings/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rating(
    rating_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    rating = await db.get(MediaRating, rating_id)

    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    if rating.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the user who created this rating can delete it",
        )

    await db.delete(rating)
    await db.commit()

    return None