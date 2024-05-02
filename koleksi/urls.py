from django.urls import path
from . import views

urlpatterns = [
    path('daftar_kontributor/', views.contributor_list_view, name='contributor_list'),
    path('daftar_unduhan/', views.daftar_unduhan_view, name='daftar_unduhan'),
   path('daftar_favorit/', views.daftar_favorit_view, name='daftar_favorit'), # Map the view to the root URL of the app
]