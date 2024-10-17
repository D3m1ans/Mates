from django.urls import path, include
from .views import custom_login_view

urlpatterns = [
    path('login/', custom_login_view, name='login'),
]
