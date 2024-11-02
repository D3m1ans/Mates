from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'password', 'birthdate',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password'],
            birthdate=validated_data.get('birthdate')
        )

        return user

class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'ui',
            'email',
            'nickname',
            'mates_points',
            'birthdate',
            'registration_date',
            'profile_description',
            'status',
            'profile_picture'
        ]

        extra_kwargs = {
            'nickname': {'required': False},
            'birthdate': {'required': False},
            'profile_description': {'required': False},
            'profile_picture': {'required': False},
            'telegram_url': {'required': False},
            'steam_url': {'required': False},
            'discord_url': {'required': False},
        }