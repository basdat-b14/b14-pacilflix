from django.urls import path
from b14_pacilflix import settings
from main.views import show_main,register,login,logout, is_authenticated
from django.conf.urls.static import static

app_name = 'main'


urlpatterns = [
    path('', show_main, name = 'show_main'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('is_authenticated/', is_authenticated, name='is_authenticated'),

    



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)