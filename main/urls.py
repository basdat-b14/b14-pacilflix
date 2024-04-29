from django.urls import path
from . import views

app_name = 'main'


urlpatterns = [
    path('', views.show_main, name = 'show_main'),
]
