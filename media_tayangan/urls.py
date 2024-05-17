from django.urls import path
from media_tayangan.views import *


app_name = 'media_tayangan'

urlpatterns = [
    path('trailer', trailer_view, name='trailer_view'),
    path('cari-trailer', cari_trailer, name='cari_trailer'),
    path('tayangan', tayangan_view, name='tayangan_view'),
    path('cari-tayangan', cari_tayangan, name='cari_tayangan'),
    path('series/<str:judul>/', series_view, name='series_view'),
    path('film/<str:judul>/', film_view, name='film_view'),
    path('episode', episode_view, name='episode_view'),
]