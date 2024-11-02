from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, PasswordResetRequestView, PasswordResetConfirmView, UserProfileView, \
    UserProfileUpdateView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterAPIView.as_view(), name='register_api'),

    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uid64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('profile/', UserProfileView.as_view(), name='api-profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='api-profile-update'),
]
