from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

# Create your models here.
class Entry(models.Model):
    """Model representing an entry for a checklist."""
    name = models.CharField(max_length=200, unique=True, help_text="Add and entry to your list.")

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


class Checklist(models.Model):
    """Model representing a checklist."""
    title = models.CharField(max_length=100, default='New List')
    category = models.CharField(max_length=100, null=True, blank=True)
    entry = models.ManyToManyField(Entry, help_text="Add an entry to your list.")
    due_date = models.DateField(null=True, blank=True)



    def __str__(self):
        """String for representing the Model object."""
        return self.title