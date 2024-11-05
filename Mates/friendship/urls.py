# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('friends/', views.friend_list, name='friend_list'),
    path('send-request/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:friendship_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('delete-friend/<int:friendship_id>/', views.delete_friend, name='delete_friend'),
    path('block-user/<int:friendship_id>/', views.block_user, name='block_user'),
]
