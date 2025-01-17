from django.utils import timezone # (to add date for when to 'complete' checklist, e.g. when to go shopping)
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings
import uuid

# Create your models here.

# def shopping_day():
#     return  *find days from sunday* eg. one week from now is: timezone.now() + timezone.timedelta(days=7) 

### future - could create different types of lists instead of one checklist.  eg. grocery list, to-do, gift ideas, etc

class Checklist(models.Model):  
    """Model representing a checklist."""
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        """overwrites the internal save() method to automatically create a slug, if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("checklist-detail", args=[str(self.slug)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    

class Entry(models.Model):
    """Model representing an entry for a checklist."""

    name = models.CharField(max_length=200, unique=True, help_text="Add an entry to your list.")
    notes = models.TextField(null=True, blank=True)  # maybe change to CharField
    # due_date = models.DateTimeField(null=True, blank=True)
    # sub_category = models.CharField(max_length=100, null=True, blank=True)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, null=True)      ### maybe change to ManytoManyField later?
    ## quantity

    def get_absolute_url(self):
        return reverse(
            "entry-update", args=[str(self.checklist.id), str(self.id)]
        )

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='entry_name_case_insensitive_unique',
                violation_error_message = "Entry already exists (case insensitive match)"
            ),
        ]
