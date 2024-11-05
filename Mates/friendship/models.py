from django.db import models
from django.conf import settings

# Create your models here.

class Friendship(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='send_friend_request', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_request', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('blocked', 'Blocked')], default='pending')
    created_ad = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"