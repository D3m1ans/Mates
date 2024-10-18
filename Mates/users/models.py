import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        extra_fields.setdefault('registration_date', timezone.now())
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('banned', 'Banned'),
        ('pending', 'Pending'),
    ]

    username = None
    ui = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50)
    birthdate = models.DateField(null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)
    profile_description = models.TextField(null=True, blank=True)
    mates_points = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    is_staff = models.BooleanField(default='False')
    is_active = models.BooleanField(default='True')

    telegram_url = models.URLField(null=True, blank=True)
    steam_url = models.URLField(null=True, blank=True)
    discord_url = models.URLField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'birthdate']

    objects = CustomUserManager()

    def __str__(self):
        return self.email