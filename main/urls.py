from django.urls import path
from b14_pacilflix import settings
from . import views
from django.conf.urls.static import static

app_name = 'main'


urlpatterns = [
    path('', views.show_main, name = 'show_main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)