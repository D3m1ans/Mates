from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import custom_login_view, main, register, custom_logout, profile_view, edit_profile_view

urlpatterns = [
    path('', main, name='main'),
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile-edit/', edit_profile_view, name='edit_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
