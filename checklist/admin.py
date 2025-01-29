from django.contrib import admin
from .models import Profile, Checklist, Entry

# Register your models here.
admin.site.register(Checklist)
admin.site.register(Entry)
admin.site.register(Profile)