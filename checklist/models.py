from django.utils import timezone # (to add date for when to 'complete' checklist, e.g. when to go shopping)
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver




# Create your models here.

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     friends = models.ManyToManyField(
#         "self",
#         related_name="friends_with",
#         symmetrical=False,
#         blank=True
#     )

#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()

#     def __str__(self):
#         return self.user.username


# class FriendRequest(models.Model):
#     sender = models.ForeignKey(Profile, related_name='sent_requests', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(Profile, related_name='received_requests', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.sender.user.username

#     class Meta:
#         unique_together = ('sender', 'receiver')


class Checklist(models.Model):  
    """Model representing a checklist."""
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """overwrites the internal save() method to automatically create a slug, if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("list", kwargs=[str(self.author.username), str(self.slug)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    

class Entry(models.Model):
    """Model representing an entry for a checklist."""

    name = models.CharField(max_length=100, help_text="Add an entry to your list.")
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)

    creation_date = models.DateTimeField('date created', auto_now_add=True, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    # notes = models.TextField(null=True, blank=True)  # maybe change to CharField # or change to quantity
    # sub_category = models.CharField(max_length=100, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("entry-update", kwargs=[str(self.checklist.author.username), str(self.checklist.slug), str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    class Meta:
        ordering = ['creation_date']

