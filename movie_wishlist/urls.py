
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/categories/', include('categories.urls')),
    path('api/movies/', include('movies.urls')),
    path('api/watchlist/', include('watchlist.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/auth/', include('accounts.urls')),

    # --- JWT Auth Endpoints ---
    # POST {"username", "password"} -> {"access", "refresh"}
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    # POST {"refresh"} -> new {"access"}
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

     # --- Swagger - Documentation Endpoints (drf-spectacular) ---
    # 1. Schema: Generates the raw OpenAPI JSON file (Machine Readable)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # 2. Swagger UI: Interactive Interface for testing APIs (Developer Friendly)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # 3. Redoc: Clean, Organize documentation for reading (User Friendly)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

# Serve uploaded files in DEVELOPMENT (static() returns [] when DEBUG=False —
# in production a web server / cloud storage serves media, never Django).
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
