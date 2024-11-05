# views.py
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Friendship

User = get_user_model()

@login_required
def send_friend_request(request):
    email = request.GET.get('email')

    if not email:
        messages.error(request, "Email is required to send a friend request.")
        return redirect('friend_list')

    # Поиск пользователя по email
    try:
        receiver = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "User with this email does not exist.")
        return redirect('friend_list')

    # Проверка, что пользователь не отправляет запрос самому себе
    if receiver == request.user:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('friend_list')

    # Проверка на наличие уже существующего запроса
    friendship, created = Friendship.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={'status': 'pending'}
    )

    if not created:
        messages.info(request, "Friend request already sent.")
    else:
        messages.success(request, "Friend request sent successfully.")

    return redirect('friend_list')

@login_required
def accept_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, receiver=request.user)
    friendship.status = 'accepted'
    friendship.save()
    return redirect('friend_list')

@login_required
def delete_friend(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)
    if friendship.sender == request.user or friendship.receiver == request.user:
        friendship.delete()
    return redirect('friend_list')

@login_required
def block_user(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, sender=request.user)
    friendship.status = 'blocked'
    friendship.save()
    return redirect('friend_list')

@login_required
def friend_list(request):
    friendships = Friendship.objects.filter(
        (Q(sender=request.user) | Q(receiver=request.user)),
        status='accepted'
    )
    friend_requests = Friendship.objects.filter(receiver=request.user, status='pending')
    context = {
        'friendships': friendships,
        'friend_requests': friend_requests,
    }
    return render(request, 'friendship/friend_list.html', context)
