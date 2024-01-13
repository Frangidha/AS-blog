from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls'), name='about'),
    path('mas/', include('mas.urls'), name='mas'),
    path('', include('blog.urls'), name='blog'),
    path('profiles/', include('profiles.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('allauth.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
