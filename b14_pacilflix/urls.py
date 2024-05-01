from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('media_tayangan/', include('media_tayangan.urls')),
]