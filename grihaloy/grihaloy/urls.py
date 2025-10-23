from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 Homepage (newly created app)
    path('', include(('home.urls', 'home'), namespace='home')),

    # 👇 Users app
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('properties/', include(('properties.urls', 'properties'), namespace='properties')),
    path('heatmap/', include('heatmap_service.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
