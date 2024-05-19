from django.urls import path
from . import views
from main.views import *
import uuid

app_name = 'koleksi'

urlpatterns = [
    # path('daftar_kontributor/', views.contributor_list_view, name='contributor_list'),
    path('daftar_unduhan/', views.daftar_unduhan_view, name='daftar_unduhan'),
    path('daftar_favorit/', views.daftar_favorit_view, name='daftar_favorit'), # Map the view to the root URL of the app

    # path('delete_tayangan/', views.delete_tayangan, name='delete_tayangan'),
    path('delete_unduhan/<str:nama_tayangan>/<str:username>/<uuid:id_tayangan>/', views.delete_unduhan, name='delete_unduhan')

    # path('contributors/', views.contributors_list, name='contributor_list'),
    path('daftar_kontributor/', views.contributors_list, name='daftar_kontributor_page'),



]