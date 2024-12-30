from django.db import models

# Create your models here.
class Checklist(models.Model):
    """Model representing an item on a checklist."""
    entry = models.TextField()