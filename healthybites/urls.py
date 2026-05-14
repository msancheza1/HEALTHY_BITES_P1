from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('planner.urls')),
    path('accounts/', include('accounts.urls')),
    path('recipes/', include('recipes.urls', namespace='recipes')), 
    path('accounts/', include('django.contrib.auth.urls')),
]

# Servir media files en ambos modos (debug y producción)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# En producción, también servir estáticos como fallback
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)