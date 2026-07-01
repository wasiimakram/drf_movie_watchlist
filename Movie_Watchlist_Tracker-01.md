# 🎬 Movie Watchlist API — Learning Tracker

> **Stack:** Django 5 · DRF · PostgreSQL · JWT  
> **Level:** Frontend Developer learning Backend  
> **Style:** Step by step — nothing skipped

---

## 📊 Overall Progress

| Phase | Status |
|---|---|
| Phase 1 — Core Build | 🔄 In Progress |
| Phase 2 — Enhancements | ⏳ Not Started |

---

## 🗺️ Phase 1 — Build Steps Overview

| Step | Task | Status |
|---|---|---|
| 1 | Project Setup | 🔄 In Progress |
| 2 | Category Model + CRUD | ✅ Done |
| 3 | Movie Model + M2M Category | 🔄 In Progress |
| 4 | Authentication — JWT | ⏳ Not Started |
| 5 | Watchlist — CRUD + CSV Export | ⏳ Not Started |
| 6 | Reviews — CRUD | ⏳ Not Started |
| 7 | Django Signals + Notifications | ⏳ Not Started |
| 8 | Dashboard + Analytics | ⏳ Not Started |
| 9 | Full-Text Search | ⏳ Not Started |
| 10 | Swagger Docs + README | ⏳ Not Started |

---

## ✅ Step 1 — Project Setup

### 🎯 Goal
Set up a clean Django project connected to PostgreSQL with all Phase 1 packages installed.

### 📋 Checklist
- [ ] Install Python (if not installed)
- [ ] Install PostgreSQL (if not installed)
- [ ] Install VS Code (if not installed)
- [ ] Create project folder
- [ ] Create and activate virtual environment
- [ ] Install all required packages
- [ ] Create `.env` file
- [ ] Create Django project
- [ ] Connect PostgreSQL database in settings
- [ ] Run first migration
- [ ] Verify server runs on `http://127.0.0.1:8000`

### 🛠️ Commands

#### 1.1 — Create project folder
```bash
mkdir movie_watchlist
cd movie_watchlist
```

#### 1.2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

> ✅ You should see `(venv)` at the start of your terminal line

#### 1.3 — Install all packages
```bash
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular django-filter psycopg2-binary python-decouple
```

## Packages Overview

| Package | Purpose |
|----------|----------|
| **django** | Main web framework (Models, Views, URLs, Auth, Admin) |
| **djangorestframework** | Build REST APIs (Serializers, API Views, Permissions) |
| **djangorestframework-simplejwt** | JWT Authentication (Access & Refresh Tokens) |
| **drf-spectacular** | Auto-generate Swagger & ReDoc API documentation |
| **django-filter** | Add filtering support to APIs (`?category=1`) |
| **psycopg2-binary** | PostgreSQL database driver for Django |
| **python-decouple** | Manage `.env` variables securely |


#### 1.4 — Save installed packages
```bash
pip freeze > requirements.txt
```

#### 1.5 — Create Django project
```bash
django-admin startproject movie_watchlist .
```

> ✅ The `.` at the end is important — it creates the project in the current folder

#### 1.6 — Create `.env` file
Create a file called `.env` in your root folder with this content:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=movie_watchlist
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

#### 1.7 — Create PostgreSQL database
Open **pgAdmin** or **psql** and run:
```sql
CREATE DATABASE movie_watchlist;
```

#### 1.8 — Update `movie_watchlist/settings.py`
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',   # For Full-Text Search later
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

#### 1.9 — Run first migration
```bash
python manage.py migrate
```

#### 1.10 — Start server
```bash
python manage.py runserver
```

> ✅ Open browser → `http://127.0.0.1:8000` — you should see Django welcome page

### 📝 Notes & Issues
> _(Add any errors or notes here as you go)_

### ✅ Step 1 Status: ✅ Complete

---

## 🔄 Step 2 — Category Model + CRUD

### 🎯 Goal
Create the `categories` app with a Category model, then build full CRUD API endpoints — List, Create, Detail, Update, Delete.

### 💡 What is an App in Django?
Django projects are made of small **apps** — each app handles one feature.
- `categories` app → handles everything about categories
- Later: `movies` app, `watchlist` app etc.
- Each app has: `models.py` → `serializers.py` → `views.py` → `urls.py`

### 📋 Checklist
- [x] Create `categories` app
- [x] Register app in `settings.py`
- [x] Write Category model in `models.py`
- [x] Run migrations for Category
- [x] Write CategorySerializer in `serializers.py`
- [x] Write CategoryView in `views.py`
- [x] Write URLs in `categories/urls.py`
- [x] Connect to main `movie_watchlist/urls.py`
- [x] Test all endpoints in Swagger

### 🛠️ Commands & Code

#### 2.1 — Create the categories app
```bash
python manage.py startapp categories
```

> ✅ This creates a `categories/` folder with all the Django files inside

#### 2.2 — Register app in `movie_watchlist/settings.py`
Add `'categories'` to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'django.contrib.postgres',
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    # Our apps
    'categories',   # ← add this
]
```

#### 2.3 — Write Category model in `categories/models.py`
```python
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Auto-generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
```

> 💡 `slugify('Action Movies')` → `'action-movies'` automatically

#### 2.4 — Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

> ✅ Check pgAdmin — you should see a `categories_category` table

#### 2.5 — Register in `categories/admin.py`
```python
from django.contrib import admin
from .models import Category

admin.site.register(Category)
```

> ✅ Now you can see and manage categories in Django Admin

#### 2.6 — Write CategorySerializer in `categories/serializers.py`
Create a new file `categories/serializers.py`:
```python
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['slug', 'created_at']
```

> 💡 Serializer converts your Python model → JSON for the API response

#### 2.7 — Write CategoryViews in `categories/views.py`
We use **separate generic views** for each group of operations — this keeps it clear which view handles what, instead of one view doing everything automatically.

```python
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/categories/   -> List all categories
    POST /api/categories/   -> Create a new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/categories/{id}/  -> Get one category
    PUT    /api/categories/{id}/  -> Full update
    PATCH  /api/categories/{id}/  -> Partial update
    DELETE /api/categories/{id}/  -> Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
```

> 💡 `generics.ListCreateAPIView` = handles GET (list) + POST in one class
> 💡 `generics.RetrieveUpdateDestroyAPIView` = handles GET (single) + PUT + PATCH + DELETE in one class
> This is the middle ground between writing 5 separate views and using one auto-magic `ModelViewSet` — you can clearly see which class is responsible for which group of operations.

#### 2.8 — Write `categories/urls.py`
Create a new file `categories/urls.py`. No router needed — URLs are defined manually for clarity:
```python
from django.urls import path
from .views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
```

#### 2.9 — Connect to main `movie_watchlist/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/', include('categories.urls')),
    # Swagger docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

#### 2.10 — Run server and test
```bash
python manage.py runserver
```

Open Swagger UI → `http://127.0.0.1:8000/api/schema/swagger-ui/`

You should see these endpoints:
| Method | Endpoint | Handled By |
|---|---|---|
| GET | `/api/categories/` | `CategoryListCreateView` |
| POST | `/api/categories/` | `CategoryListCreateView` |
| GET | `/api/categories/{id}/` | `CategoryDetailView` |
| PUT/PATCH | `/api/categories/{id}/` | `CategoryDetailView` |
| DELETE | `/api/categories/{id}/` | `CategoryDetailView` |

### 📝 Notes & Issues
> **Structure decision:** Project renamed `config` → `movie_watchlist` to match Expense Tracker pattern. After renaming, 3 files needed manual fixes: `manage.py`, `movie_watchlist/wsgi.py` (both pointed to `config.settings`), and `movie_watchlist/settings.py` (`ROOT_URLCONF` and `WSGI_APPLICATION` pointed to `config.urls`/`config.wsgi`).
>
> **Views decision:** Switched from `ModelViewSet` + `DefaultRouter` to separate `generics.ListCreateAPIView` + `generics.RetrieveUpdateDestroyAPIView` with manual URL patterns — easier to see what each endpoint does while learning.
>
> **Bug fixed:** `AttributeError: 'list' object has no attribute 'values'` on `GET /api/categories/`. Cause: `model`, `fields`, `read_on_fields` were written directly on the `CategroySerializer` class instead of nested inside a `class Meta:`. Also had a typo `read_on_fields` → should be `read_only_fields`. Fixed by wrapping them in `Meta` and correcting the typo.

### ✅ Step 2 Status: ✅ Complete

---

## 🔄 Step 3 — Movie Model + M2M Category

### 🎯 Goal
Create the `movies` app with a Movie model that has a **Many-to-Many** relationship with Category (one movie can belong to multiple categories, one category can have multiple movies), then build full CRUD API endpoints.

### 💡 What is Many-to-Many (M2M)?
- A movie like "Inception" can be both **Sci-Fi** AND **Thriller** → multiple categories per movie
- The category **Sci-Fi** can have many movies → multiple movies per category
- Django handles this with `models.ManyToManyField()` — it auto-creates a hidden "join table" in the database to track these relationships, you don't write any SQL for it

### 📋 Checklist
- [x] Create `movies` app
- [x] Register app in `settings.py`
- [x] Write Movie model in `models.py` with M2M to Category
- [x] Run migrations for Movie
- [x] Register in `movies/admin.py`
- [x] Write MovieSerializer in `serializers.py` (+ nested `category_detail`, read-only)
- [x] Write MovieViews in `views.py` (List/Create + Detail/Update/Delete)
- [x] Write URLs in `movies/urls.py`
- [x] Connect to main `movie_watchlist/urls.py`
- [ ] Test all endpoints in Swagger

> ✅ **CRUD complete.** Before moving to Step 4, we're loading this Movie app up with as many Level 2/3 DRF concepts as make sense (filtering, ordering, search, pagination, N+1 optimization, etc. — see the Concept Master List below) to get max learning value out of it first.

### 🛠️ Commands & Code

#### 3.1 — Create the movies app
```bash
python manage.py startapp movies
```

#### 3.2 — Register app in `movie_watchlist/settings.py`
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    # Our apps
    'categories',
    'movies',   # ← add this
]
```

#### 3.3 — Write Movie model in `movies/models.py`
```python
from django.db import models
from categories.models import Category


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    category = models.ManyToManyField(Category, related_name='movies')
    director = models.CharField(max_length=200)
    plot = models.TextField(blank=True)
    poster_url = models.URLField(blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    runtime_minutes = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

> 💡 `related_name='movies'` lets you do `category.movies.all()` later to get all movies in a category
> 💡 `ManyToManyField` does NOT need a `ForeignKey` — Django creates the join table automatically

#### 3.4 — Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

> ✅ Check pgAdmin — you should see a `movies_movie` table AND a hidden `movies_movie_category` join table

#### 3.5 — Register in `movies/admin.py`
```python
from django.contrib import admin
from .models import Movie

admin.site.register(Movie)
```

#### 3.6 — Write MovieSerializer in `movies/serializers.py`
```python
from rest_framework import serializers
from .models import Movie
from categories.serializers import CategorySerializer


class MovieSerializer(serializers.ModelSerializer):

    # Nested serializer for rich response (Read-only)
    category_detail = CategorySerializer(source='category', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'year', 'category', 'category_detail', 'director', 'plot',
            'poster_url', 'imdb_rating', 'runtime_minutes',
            'language', 'country', 'created_at'
        ]
        read_only_fields = ['created_at']
```

> 💡 `category` stays a **writable** list of category IDs, e.g. `"category": [1, 3]`, for POST/PATCH. `category_detail` is a **read-only nested** field that shows the full category objects on GET — this is the "Nested Serialization" concept (Level 1, #3).

#### 3.7 — Write MovieViews in `movies/views.py`
Same pattern as Categories — separate views for clarity. `permission_classes` is left off both views for now since JWT auth doesn't exist yet (Step 4):

```python
from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer


class MovieListAndCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/movies --> List all movies
    POST /api/movies --> Create a new movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailAndUpdateAndDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve specific movie
    PUT/PATCH: Update movie
    PATCH: In patch, we can only pass specific value that needs to be updated
    PUT: In PUT we need to send the whole object to update even 1 value.
    DELETE: Delete movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
```

#### 3.8 — Write `movies/urls.py`
```python
from django.urls import path, include
from .views import (
    MovieListAndCreateAPIView,
    MovieDetailAndUpdateAndDeleteAPIView,
)

urlpatterns = [
    # POST, GET List
    path('', MovieListAndCreateAPIView.as_view(), name='movie-list'),

    # GET, PUT, PATCH, DELETE
    path('<int:pk>/', MovieDetailAndUpdateAndDeleteAPIView.as_view(), name='movie-detail'),
]
```

> 💡 The main `movie_watchlist/urls.py` mounts this at `path('api/movies/', include('movies.urls'))`, so these blank/`<pk>/` patterns become `/api/movies/` and `/api/movies/<pk>/`.

#### 3.9 — Connect to main `movie_watchlist/urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/', include('categories.urls')),
    path('api/', include('movies.urls')),   # ← add this
    # Swagger docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

#### 3.10 — Run server and test
```bash
python manage.py runserver
```

Open Swagger UI → `http://127.0.0.1:8000/api/schema/swagger-ui/`

You should see these endpoints:
| Method | Endpoint | Handled By |
|---|---|---|
| GET | `/api/movies/` | `MovieListAndCreateAPIView` |
| POST | `/api/movies/` | `MovieListAndCreateAPIView` |
| GET | `/api/movies/{id}/` | `MovieDetailAPIView` |
| PUT/PATCH | `/api/movies/{id}/` | `MovieDetailAPIView` |
| DELETE | `/api/movies/{id}/` | `MovieDetailAPIView` |

**Test data for POST `/api/movies/`** (use category IDs you created in Step 2):
```json
{
  "title": "Inception",
  "year": 2010,
  "category": [1, 2],
  "director": "Christopher Nolan",
  "plot": "A thief who steals corporate secrets through dream-sharing technology.",
  "imdb_rating": 8.8,
  "runtime_minutes": 148,
  "language": "English",
  "country": "USA"
}
```

### 📝 Notes & Issues
> _(Add any errors or notes here as you go)_

### ✅ Step 3 Status: 🔄 In Progress

---

## ⏳ Step 4 — Authentication (JWT)
> Will be detailed once Step 3 is complete ✅

---

## ⏳ Step 5 — Watchlist CRUD + CSV Export
> Will be detailed once Step 4 is complete ✅

---

## ⏳ Step 6 — Reviews CRUD
> Will be detailed once Step 5 is complete ✅

---

## ⏳ Step 7 — Django Signals + Notifications
> Will be detailed once Step 6 is complete ✅

---

## ⏳ Step 8 — Dashboard + Analytics
> Will be detailed once Step 7 is complete ✅

---

## ⏳ Step 9 — Full-Text Search
> Will be detailed once Step 8 is complete ✅

---

## ⏳ Step 10 — Swagger Docs + README
> Will be detailed once Step 9 is complete ✅

---

## 🔜 Phase 2 — Enhancements (Later)
- [ ] Admin Role + RBAC
- [ ] OMDB External API Integration
- [ ] Caching
- [ ] Unit Testing with pytest-django

---

## 💡 Quick Reference

### Useful Commands
```bash
python manage.py runserver        # Start server
python manage.py makemigrations   # Create migrations
python manage.py migrate          # Apply migrations
python manage.py createsuperuser  # Create admin user
python manage.py shell            # Django shell
```

### Useful URLs (once server is running)
| URL | What it is |
|---|---|
| `http://127.0.0.1:8000/admin/` | Django Admin Panel |
| `http://127.0.0.1:8000/api/schema/swagger-ui/` | Swagger UI |
| `http://127.0.0.1:8000/api/schema/redoc/` | ReDoc |

---

## 🧠 DRF Concept Master List

> Pick one concept at a time. Each one will be implemented in the project with full explanation and code.
> Status: ⏳ Not Started · 🔄 In Progress · ✅ Done

---

### 🟢 Level 1 — Basics
| # | Concept | Status | Learned In |
|---|---|---|---|
| 1 | Models + Migrations | ✅ Done | Step 1–3 |
| 2 | Serializers + ModelSerializer | ✅ Done | Step 2–3 |
| 3 | Nested Serialization (`category_detail`) | ✅ Done | Step 3 |
| 4 | Generic Views (ListCreate, RetrieveUpdateDestroy) | ✅ Done | Step 2–3 |
| 5 | URL Routing | ✅ Done | Step 2–3 |
| 6 | Django Admin | ✅ Done | Step 2–3 |
| 7 | Environment Variables (`python-decouple`) | ✅ Done | Step 1 |

---

### 🟡 Level 2 — Core API Skills
| # | Concept | Status | Learned In |
|---|---|---|---|
| 8 | Advanced Filtering (`django-filter`) | 🔄 In Progress | Movie |
| 9 | N+1 Optimization (`prefetch_related` / `select_related`) | ⏳ | Movie |
| 10 | Custom QuerySet / Manager | ⏳ | Movie |
| 11 | DRF Built-in Search + Ordering Filters | ⏳ | Movie |
| 12 | Full-Text Search (PostgreSQL `SearchVector`) | ⏳ | Movie |
| 13 | Pagination | ⏳ | Movie |
| 14 | Throttling | ⏳ | Movie |
| 15 | JWT Authentication | ⏳ | Step 4 — Auth app |
| 16 | Data Isolation (custom Mixins) | ⏳ | Step 5 — Watchlist |
| 17 | CSV Export | ⏳ | Step 5 — Watchlist |
| 18 | Django Signals | ⏳ | Step 7 — Notifications |

---

### 🔵 Level 3 — Intermediate Skills
| # | Concept | Status | Learned In |
|---|---|---|---|
| 19 | Validation in Serializers | ⏳ | Movie |
| 20 | SerializerMethodField (computed fields) | ⏳ | Movie |
| 21 | Custom Actions (`@action` decorator) | ⏳ | Movie |
| 22 | ViewSet vs APIView vs Generics — when to use each | ⏳ | Movie |
| 23 | Response Shaping (different serializers for list vs detail) | ⏳ | Movie |
| 24 | Multi-field Ordering (`?ordering=-imdb_rating,year`) | ⏳ | Movie |
| 25 | Writable Nested Serializers | ⏳ | Step 5 — Watchlist |
| 26 | Custom Permissions | ⏳ | Step 4 — Auth app |

---

### 🔴 Level 4 — Advanced Skills (Phase 2 + Beyond)
| # | Concept | Status | Learned In |
|---|---|---|---|
| 27 | Caching (Redis) | ⏳ | Phase 2 |
| 28 | External API Integration (OMDB) | ⏳ | Phase 2 |
| 29 | Unit Testing with `pytest-django` | ⏳ | Phase 2 |
| 30 | Factory Boy (test data generation) | ⏳ | Phase 2 |
| 31 | Custom Exception Handling | ⏳ | Phase 2 |
| 32 | Soft Delete | ⏳ | Phase 2 |
| 33 | Audit Logging (track who changed what) | ⏳ | Phase 2 |
| 34 | API Versioning (`/api/v1/` vs `/api/v2/`) | ⏳ | Phase 2 |
| 35 | File Uploads (images/documents) | ⏳ | Phase 2 |
| 36 | Celery + Background Tasks | ⏳ | Phase 2 |
| 37 | Rate Limiting per User (free vs premium) | ⏳ | Phase 2 |
| 38 | Multi-Tenancy | ⏳ | Phase 2 |

---

> 💡 **Reminder — concepts that need Auth/Watchlist to exist first:**
> - 🔐 JWT Auth + Data Isolation → Step 4 & 5
> - 🔔 Django Signals → Step 7
> - 📤 CSV Export → Step 5
> - 🛡️ Custom Permissions + RBAC → Phase 2
