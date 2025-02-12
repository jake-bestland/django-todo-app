from django.db import models
from django.utils import timezone
from checklist.models import Profile

# Create your models here.
class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.user.username

    class Meta:
        unique_together = ('sender', 'receiver')
