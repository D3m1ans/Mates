from django.db import models
from django.conf import settings

# Create your models here.


class Game(models.Model):

    PLATFORM_CHOICES = [
        ('pc', 'PC'),
        ('ps5', 'PS5'),
        ('ps4', 'PS4'),
        ('xbox', 'Xbox'),
        ('nintendo switch', 'Nintendo Switch')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    release_data = models.DateTimeField(blank=True, null=True)
    platform = models.CharField(max_length=20,
                                choices=PLATFORM_CHOICES,
                                blank=True,
                                null=True,
                                default='pc')

    def __str__(self):
        return self.title

class UserLibrary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='library')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    playtime_hours = models.PositiveIntegerField(default=0)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    last_played = models.DateField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user} - {self.game}"

