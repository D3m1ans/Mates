from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings

from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from users.models import CustomUser
import logging

# Create your views here.

logger = logging.getLogger(__name__)

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(str(user.ui)))
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