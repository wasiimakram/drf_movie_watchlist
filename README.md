# 🎬 Movie Watchlist API

A REST API for tracking movies, personal watchlists, and reviews, built with **Django REST Framework**.
This project demonstrates modern backend practices including JWT authentication, role-based catalog access, background jobs, caching, and interactive documentation.

## 🚀 Features

### 🔐 Authentication & Security
- **JWT Authentication**: Secure stateless auth using `simplejwt` (Register, Login, Refresh).
- **Email Activation**: New accounts start inactive; a signed, self-expiring link activates them.
- **Role-Based Catalog Access**:
    - **Admin**: Full control over movies and categories (create/update/delete).
    - **User**: Read-only on the shared catalog, full control over their own data.
- **Data Isolation**: Row-level security powered by a custom mixin — watchlist, reviews, and notifications are private per user.
- **Throttling**: Per-user rate limiting on movie endpoints.

### 🎥 Core Functionality
- **Movies & Categories**: Full CRUD, with a many-to-many category relationship.
- **Watchlist**: Personal, with status tracking (`want_to_watch` / `watching` / `watched`).
- **Reviews**: Star ratings + text, one per user per movie, plus a public "all reviews for this movie" endpoint.
- **Posters**: Image upload support for movies.
- **Advanced Filtering**: Filter by year, rating, runtime, category, director, language, country; free-text search; multi-field ordering; pagination.

### 🔔 Notifications
- **Event-Driven**: Automatically generated when a movie is added to a watchlist or marked watched.
- **Architecture**: Powered by **Django Signals** (decoupled logic — no app imports another to notify).
- **In-App**: Unread status and history list.

### 🔄 Data Management
- **External Import**: Pull full movie data (plot, rating, runtime, poster, genres) from OMDB by title alone.
- **Bulk Import**: Queue multiple OMDB imports as background jobs — one bad title never blocks the batch.
- **Nested Writes**: Mark a movie watched and submit its review in a single request.

### 📚 Documentation
- **Swagger UI**: Interactive API testing interface via `drf-spectacular`.
- **ReDoc**: Clean, organized API reference.

### ⚡ Performance & Architecture
- **Optimization**: N+1 queries eliminated using `prefetch_related`, wrapped in a custom queryset method.
- **Caching**: Redis-backed response caching on the shared catalog endpoints.
- **Background Jobs**: Celery + Redis queue for bulk imports, decoupled from the request/response cycle.
- **Consistent Error Format**: Every API error returns the same shape — `{success, status_code, errors}`.
- **Nested Serialization**: Movies embed their categories, watchlist embeds movie details, reviews embed movie or author depending on the endpoint.
- **Clean Architecture**: Shared mixins, permissions, and exception handling centralized in a `core` app.

---

## 🛠️ Technology Stack

- **Framework**: Django 6 + Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Auth**: `djangorestframework-simplejwt`
- **Docs**: `drf-spectacular` (OpenAPI 3.0)
- **Utilities**: `django-filter`, `Pillow`, `requests`
- **Async**: `Celery` + `Redis`

---

## ⚡ Getting Started

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd movie_wishlist

# Create Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=movie_watchlist
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
OMDB_API_KEY=your-omdb-api-key
```

### 4. Start Redis
```bash
brew services start redis   # macOS/Homebrew
```

### 5. Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```

### 7. Start the Celery Worker
Required for bulk movie import (in a separate terminal):
```bash
celery -A movie_wishlist worker --loglevel=info
```

---

## 📖 API Documentation

Once the server is running, explore the APIs at:
- **Swagger UI**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- **ReDoc**: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

### Key Endpoints

| Endpoint | Description |
|---|---|
| `POST /api/auth/register/` | Create an account (sends activation email) |
| `GET /api/auth/activate/<uidb64>/<token>/` | Activate an account |
| `POST /api/token/` | Obtain access + refresh tokens |
| `GET/POST /api/categories/` | List / create categories (write: admin only) |
| `GET/POST /api/movies/` | List (filter/search/sort/paginate) / create movies (write: admin only) |
| `POST /api/movies/import-from-omdb/` | Import one movie from OMDB (admin only) |
| `POST /api/movies/bulk-import/` | Queue background import of multiple movies (admin only) |
| `GET /api/movies/<id>/reviews/` | All reviews for one movie |
| `GET/POST /api/watchlist/` | Manage your own watchlist |
| `GET/POST /api/reviews/` | Manage your own reviews |
| `GET /api/notifications/` | Your notifications |

---

## 🧪 Testing

```bash
# Run Unit Tests (Coming Soon)
python manage.py test
```
