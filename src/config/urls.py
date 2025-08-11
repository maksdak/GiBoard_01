# src/config/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include # <-- Added 'include'

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # API v1
    # This line includes all URLs from the 'api' app under the 'api/v1/' prefix.
    path('api/v1/', include('api.urls', namespace='api')),
]

# --- Media Files Serving (for development) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)