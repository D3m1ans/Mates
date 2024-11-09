from rest_framework import serializers
from .models import Friendship
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendshipSerializer(serializers.ModelSerializer):
    sender = serializers.EmailField(source='sender.email', read_only=True)
    receiver = serializers.EmailField(source='receiver.email', read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'status']

class SendFriendRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class AcceptFriendshipRequestSerializer(serializers.Serializer):
    friendship_id = serializers.IntegerField()

class DeclineFriendshipRequestSerializer(serializers.Serializer):
    friendship_id = serializers.IntegerField()