from django.urls import path, include
from .views import custom_login_view, main, register, custom_logout, profile_view, edit_profile_view

urlpatterns = [
    path('', main, name='main'),
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile-edit/', edit_profile_view, name='edit_profile')
]
