from django.urls import path
from b14_pacilflix import settings
from main.views import login, register, show_main
from django.conf.urls.static import static

app_name = 'main'


urlpatterns = [
    path('', show_main, name = 'show_main'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)