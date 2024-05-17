from django.urls import path
from main.views import *
from . import views


app_name = 'users'

urlpatterns = [
    path('langganan/', views.subscription_page, name='subscription_page'),  # Map the view to the root URL of the app
    path('langganan/<package_type>/', views.buy_package, name='buy_package'),
 


]