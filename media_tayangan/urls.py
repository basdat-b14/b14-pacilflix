from django.urls import path
from media_tayangan.views import trailer_view

urlpatterns = [
    # Other URL patterns
    path('trailer_tayangan', trailer_view, name='trailer_view'),
]