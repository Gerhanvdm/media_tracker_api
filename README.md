# Media Tracker API

A beginner-friendly but realistic async REST API built with:

- Python
- FastAPI
- SQLAlchemy 2.x Async ORM
- MySQL 8
- asyncmy
- Pydantic v2
- uv
- Uvicorn

The project allows users to:

- Create users
- Add media items
- Rate movies, books, and games
- View ratings from multiple users

---

# Features

## Users

- Create users
- List users
- Fetch users by ID

## Media

- Add movies, books, and games
- Update media items
- Delete media items
- Filter by media type

## Ratings

- Rate any media item
- One rating per user per media item
- Update ratings
- Delete ratings

---

# Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | API framework |
| SQLAlchemy 2.x | ORM |
| asyncmy | Async MySQL driver |
| MySQL 8 | Database |
| Pydantic v2 | Validation |
| uv | Dependency/project management |
| Uvicorn | ASGI server |

---

# Project Structure

```text
media-tracker-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── media.py
│   │   └── rating.py
│   ├── routers/
│   │   ├── users.py
│   │   ├── media.py
│   │   └── ratings.py
│   └── schemas/
│       ├── user.py
│       ├── media.py
│       └── rating.py
├── .env
├── pyproject.toml
└── README.md
```

---

# Requirements

- Python 3.12+
- MySQL 8+
- uv

---

# Install uv

## Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Mac/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:

```bash
uv --version
```

---

# Setup

## 1. Clone the project

```bash
git clone https://github.com/Gerhanvdm/media_tracker_api.git
cd media-tracker-api
```

---

## 2. Create virtual environment

```bash
uv venv
```

Activate it.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Mac/Linux

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
uv sync
```

Or include dev dependencies:

```bash
uv sync --dev
```

---

# Configure MySQL

Make sure your local MySQL server is running.

---

## Create database

Connect as root:

```powershell
mysql -u root -p
```

Run:

```sql
CREATE DATABASE IF NOT EXISTS media_tracker;
```

---

## Create application user

```sql
CREATE USER IF NOT EXISTS 'media_user'@'localhost'
IDENTIFIED BY 'media_password';

GRANT ALL PRIVILEGES ON media_tracker.*
TO 'media_user'@'localhost';

FLUSH PRIVILEGES;
```

---

# Windows Notes

If PowerShell says:

```text
mysql : The term 'mysql' is not recognized
```

then MySQL is installed but not added to PATH.

Add this folder to your Windows PATH:

```text
C:\Program Files\MySQL\MySQL Server 8.0\bin
```

Then restart PowerShell.

You can also use MySQL Workbench instead of the CLI.

---

# Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=mysql+asyncmy://media_user:media_password@localhost:3306/media_tracker
```

Project structure should look like:

```text
media-tracker-api/
├── app/
├── .env
├── pyproject.toml
└── README.md
```

---

# Run the API

Start the FastAPI development server:

```bash
uv run uvicorn app.main:app --reload
```

API will be available at:

```text
http://localhost:8000
```

---

# API Documentation

FastAPI automatically generates interactive API docs.

## Swagger UI

```text
http://localhost:8000/docs
```

## ReDoc

```text
http://localhost:8000/redoc
```

---

# Database

The application automatically creates tables on startup using:

```python
Base.metadata.create_all()
```

Tables:

- users
- media_items
- media_ratings

---

# Models

## User

| Field | Type |
|---|---|
| id | int |
| username | string |
| email | string |
| created_at | datetime |

---

## MediaItem

| Field | Type |
|---|---|
| id | int |
| title | string |
| media_type | enum |
| creator | string |
| added_by_user_id | foreign key |
| created_at | datetime |

Media types:

- movie
- book
- game

---

## MediaRating

| Field | Type |
|---|---|
| id | int |
| media_id | foreign key |
| user_id | foreign key |
| rating | int (1-10) |
| comment | text |
| created_at | datetime |

Rules:

- A user may only rate a media item once
- Multiple users may rate the same media item

---

# API Routes

# Users

| Method | Route | Description |
|---|---|---|
| POST | `/users/` | Create user |
| GET | `/users/` | List users |
| GET | `/users/{id}` | Get user |

---

# Media

| Method | Route | Description |
|---|---|---|
| POST | `/media/` | Create media |
| GET | `/media/` | List media |
| GET | `/media/?media_type=book` | Filter media |
| GET | `/media/{id}` | Get media |
| PATCH | `/media/{id}` | Update media |
| DELETE | `/media/{id}` | Delete media |

---

# Ratings

| Method | Route | Description |
|---|---|---|
| POST | `/media/{id}/ratings` | Create rating |
| GET | `/media/{id}/ratings` | List ratings |
| PATCH | `/ratings/{id}` | Update rating |
| DELETE | `/ratings/{id}` | Delete rating |

---

# Example Requests

## Create User

### PowerShell

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/users/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "username": "gerhan",
    "email": "gerhan@example.com"
  }'
```

---

## Add Media

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/media/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "title": "Project Hail Mary",
    "media_type": "book",
    "creator": "Andy Weir",
    "added_by_user_id": 1
  }'
```

---

## List Media

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/media/" `
  -Method GET | ConvertTo-Json -Depth 10
```

---

## Filter Media

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/media/?media_type=book" `
  -Method GET | ConvertTo-Json -Depth 10
```

---

## Create Rating

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/media/1/ratings" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "user_id": 1,
    "rating": 9,
    "comment": "Amazing book"
  }'
```

---

# Common Errors

| Status | Meaning |
|---|---|
| 404 | Resource not found |
| 409 | Duplicate entry |
| 422 | Validation error |
| 403 | Forbidden action |

---

# Development Notes

## Routers

FastAPI uses `APIRouter` to split endpoints into modules.

Example:

```python
router = APIRouter(prefix="/users", tags=["Users"])
```

---

## Depends()

`Depends()` injects shared dependencies like database sessions.

```python
db: AsyncSession = Depends(get_db)
```

---

## AsyncSession

SQLAlchemy async database session used for:

- queries
- inserts
- updates
- deletes

---

## SQLAlchemy select()

Modern SQLAlchemy querying uses:

```python
result = await db.execute(select(User))
users = result.scalars().all()
```

---

## Pydantic Schemas

Schemas define:

- request validation
- API response structure

Schemas are separate from database models.

---

## model_config

Pydantic v2 uses:

```python
model_config = {"from_attributes": True}
```

This allows response schemas to read SQLAlchemy ORM objects directly.

---

## SQLAlchemy Models

Models define:

- database tables
- relationships
- constraints
- indexes

---

# Useful Commands

## Add dependency

```bash
uv add httpx
```

---

## Add dev dependency

```bash
uv add --dev pytest
```

---

## Install everything

```bash
uv sync --dev
```

---

## Run linting

```bash
uv run ruff check .
```

---

## Run tests

```bash
uv run pytest
```

---

# Future Improvements

Possible stretch goals:

- JWT authentication
- Password hashing
- Alembic migrations
- Search
- Pagination
- Sorting
- Average ratings
- Favorites/watchlists/custom groups
- Frontend
- CI/CD pipeline

---

# Learning Goals

This project teaches:

- FastAPI fundamentals
- Async Python APIs
- SQLAlchemy 2.x
- Database relationships
- REST API design
- Validation with Pydantic
- Modern Python tooling with uv

---

# License

MIT