from django.utils import timezone # (to add date for when to 'complete' checklist, e.g. when to go shopping)
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

# def shopping_day():
#     return  *find days from sunday* eg. one week from now is: timezone.now() + timezone.timedelta(days=7) 

### future - could create different types of lists instead of one checklist.  eg. grocery list, to-do, gift ideas, etc

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        "self",
        related_name="friends_with",
        symmetrical=False,
        blank=True
    )

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile(user=instance)
            user_profile.save()
            user_profile.friends.add(instance.profile)
            user_profile.save()

    def __str__(self):
        return self.user.username



class Checklist(models.Model):  
    """Model representing a checklist."""
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Profile, on_delete=models.RESTRICT, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """overwrites the internal save() method to automatically create a slug, if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("list", kwargs=[str(self.author.user), str(self.slug)])

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
        return reverse("entry-update", kwargs=[str(self.checklist.author.user), str(self.checklist.slug), str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
