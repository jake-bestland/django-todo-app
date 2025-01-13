from django.db import models

# Create your models here.
class Checklist(models.Model):
    """Model representing a checklist."""
    title = models.CharField(max_length=100, default='New List')
    category = models.CharField(max_length=100, null=True, blank=True)
    entry = models.TextField()
    due_date = models.DateField(null=True, blank=True)



    def __str__(self):
        """String for representing the Model object."""
        return self.title