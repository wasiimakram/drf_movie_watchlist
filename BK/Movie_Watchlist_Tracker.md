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
| 2 | Category Model + CRUD | ⏳ Not Started |
| 3 | Movie Model + M2M Category | ⏳ Not Started |
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
- [ ] Create `categories` app
- [ ] Register app in `settings.py`
- [ ] Write Category model in `models.py`
- [ ] Run migrations for Category
- [ ] Write CategorySerializer in `serializers.py`
- [ ] Write CategoryView in `views.py`
- [ ] Write URLs in `categories/urls.py`
- [ ] Connect to main `movie_watchlist/urls.py`
- [ ] Test all endpoints in Swagger

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

### ✅ Step 2 Status: 🔄 In Progress

---

## ⏳ Step 3 — Movie Model + M2M Category
> Will be detailed once Step 2 is complete ✅

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
