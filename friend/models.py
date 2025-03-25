# from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils import timezone
from .signals import friend_removed, friend_request_accepted, friend_request_created, friend_request_declined
# from checklist.models import Profile

# Create your models here.
class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username
    
    def add_friend(self, account):
        """ Add a new friend."""
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

            # content_type = ContentType.objects.get_for_model(self)

    def remove_friend(self, account):
        """Remove a friend."""
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, removee):
        """Initiate the action of unfriending someone."""
        remover_friends_list = self # person terminating the friendship

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(remover_friends_list.user)

        # content_type = ContentType.objects.get_for_model(self)

    def is_mutual_friend(self, friend):
        """Is this a friend? """
        if friend in self.friends.all():
            return True
        return False
    



class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver', on_delete=models.CASCADE)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """Accept a friend request. Update both SENDER and RECEIVER friend lists."""
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """Decline a friend request.  It is "declined" by setting the 'is_active' field to False."""
        self.is_active = False
        self.save()

    def cancel(self):
        """Cancel a friend request that you sent."""
        self.is_active = False
        self.save()
