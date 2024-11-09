from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, PasswordResetRequestView, PasswordResetConfirmView, UserProfileView, \
    UserProfileUpdateView, FriendshipViewSet, SendFriendshipRequestView, AcceptFriendshipRequestView, \
    DeleteFriendshipView, BlockUserView, DeclineFriendRequestView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('register/', RegisterAPIView.as_view(), name='register_api'),

    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uid64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('profile/', UserProfileView.as_view(), name='api-profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='api-profile-update'),

    path('friends/', FriendshipViewSet.as_view({'get': 'list'}), name='api_friend_list'),
    path('send-request/', SendFriendshipRequestView.as_view(), name='api_send_friend_request'),
    path('accept-request/', AcceptFriendshipRequestView.as_view(), name='api_accept_friend_request'),
    path('decline-request/', DeclineFriendRequestView.as_view(), name='api_decline_friend_request'),
    path('delete-friend/<int:friendship_id>/', DeleteFriendshipView.as_view(), name='api_delete_friend'),
    path('block-user/<int:friendship_id>/', BlockUserView.as_view(), name='api_block_user'),
]
