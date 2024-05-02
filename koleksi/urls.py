from django.urls import path
from . import views

urlpatterns = [
    path('daftar_kontributor/', views.contributor_list_view, name='contributor_list'),  # Map the view to the root URL of the app
]