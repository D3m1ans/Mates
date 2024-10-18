from django.urls import path, include
from .views import custom_login_view, main, register, custom_logout

urlpatterns = [
    path('', main, name='main'),
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout, name='logout')
]
