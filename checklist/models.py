from django.utils import timezone # (to add date for when to 'complete' checklist, e.g. when to go shopping)
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings


# Create your models here.

# def shopping_day():
#     return  *find days from sunday* eg. one week from now is: timezone.now() + timezone.timedelta(days=7) 

### future - could create different types of lists instead of one checklist.  eg. grocery list, to-do, gift ideas, etc

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)




class Checklist(models.Model):  
    """Model representing a checklist."""
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        """overwrites the internal save() method to automatically create a slug, if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("list", args=[str(self.slug)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    

class Entry(models.Model):
    """Model representing an entry for a checklist."""

    name = models.CharField(max_length=100, help_text="Add an entry to your list.")
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)  # maybe change to CharField # or change to quantity
    # due_date = models.DateTimeField(null=True, blank=True)
    # sub_category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
