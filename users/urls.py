from django.urls import path
from main.views import *
from . import views


app_name = 'users'

urlpatterns = [
    path('langganan/', views.combined_subscription_view, name='subscription_page'),  # Combined view for subscription page
    path('langganan/<package_type>/', views.buy_package, name='buy_package'),
]