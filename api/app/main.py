from fastapi import FastAPI

from app.models import Base
from app.db.database import engine
from app.routers import media, ratings, users

app = FastAPI(
    title="Media Tracker API",
    description="A practice FastAPI app for tracking and rating movies, books, and games.",
    version="0.1.0",
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Media Tracker API is running"}


app.include_router(users.router)
app.include_router(media.router)
app.include_router(ratings.router)