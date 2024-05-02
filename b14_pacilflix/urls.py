from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('media_tayangan/', include('media_tayangan.urls')),
    path('koleksi/', include('koleksi.urls')),
    path('users/', include('users.urls')),
]