from django.urls import path
from media_tayangan.views import *

urlpatterns = [
    path('trailer', trailer_view, name='trailer_view'),
    path('cari-trailer', cari_trailer, name='cari_trailer'),
    path('tayangan', tayangan_view, name='tayangan_view'),
    path('cari-tayangan', cari_tayangan, name='cari_tayangan'),
    path('series/<str:judul>/', series_view, name='series_view'),
    path('film/<str:judul>/', film_view, name='film_view'),
    path('episode/<str:judul>/', episode_view, name='episode_view'),
    path('save-progress-series', save_progress_series, name='save_progress_series'),
    path('save-progress-film', save_progress_film, name='save_progress_film'),
    path('ulasan', ulasan, name='ulasan')
]