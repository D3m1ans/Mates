from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from friendship.serializers import FriendshipSerializer, SendFriendRequestSerializer, AcceptFriendshipRequestSerializer, DeclineFriendshipRequestSerializer
from friendship.models import Friendship

from users.serializers import CustomUserSerializer, CustomUserProfileSerializer
from users.models import CustomUser

User = get_user_model()

#import logging

# Create your views here.

#logger = logging.getLogger(__name__)

class RegisterAPIView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(str(user.uid)))
            token = default_token_generator.make_token(user)

            reset_url = f"{settings.API_BASE_URL}/password-reset-confirm/{uid}/{token}/"
            send_mail(
                subject="Password Reset Request",
                message=f"To reset your password, please click the following link: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

            return Response({"uid": uid, "token": token, "message": "Password reset instructions sent to email"},
                            status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid64, token):
        password = request.data.get('password')
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = CustomUser.objects.get(ui=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        except (CustomUser.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid UID or token"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = CustomUserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendshipViewSet(viewsets.ModelViewSet):

    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            sender=self.request.user
        ) | Friendship.objects.filter(
            receiver=self.request.user
        )


class SendFriendshipRequestView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SendFriendRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                receiver  = User.objects.get(email=email)

            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if receiver == request.user:
                return Response({"error": "You cannot send a friend request to yourself."},
                                status=status.HTTP_400_BAD_REQUEST)

            friendship, created = Friendship.objects.get_or_create(
                sender=request.user,
                receiver=receiver,
                defaults={'status': 'pending'}
            )

            if not created:
                return Response({"info": "Friend request already sent."}, status=status.HTTP_200_OK)

            return Response({"success": "Friend request sent successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendshipRequestView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AcceptFriendshipRequestSerializer(data=request.data)

        if serializer.is_valid():
            friendship_id = serializer.validated_data['friendship_id']
            friendship = get_object_or_404(Friendship, id=friendship_id, receiver=request.user, status='pending')
            friendship.status = 'accepted'
            friendship.save()
            return Response({"success": "Friend request accepted."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteFriendshipView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, friendship_id):

        friendship = get_object_or_404(Friendship, id=friendship_id)

        if friendship.sender == request.user or friendship.receiver == request.user:
            friendship.delete()
            return Response({"success": "Friend deleted successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "You do not have permission to delete this friendship."},
                            status=status.HTTP_403_FORBIDDEN)

class BlockUserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, friendship_id):

        friendship = get_object_or_404(Friendship, id=friendship_id)

        if friendship.receiver == request.user or friendship.sender == request.user:
            friendship.status = 'blocked'
            friendship.save()
            return Response({"success": "User blocked successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "You do not have permission to block this friendship."}, status=status.HTTP_403_FORBIDDEN)

class DeclineFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeclineFriendshipRequestSerializer(data=request.data)
        if serializer.is_valid():
            friendship_id = serializer.validated_data['friendship_id']
            friendship = get_object_or_404(Friendship, id=friendship_id, receiver=request.user, status='pending')
            friendship.status = 'declined'
            friendship.save()
            return Response({"success": "Friend request declined."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
