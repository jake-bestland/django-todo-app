# Generated by Django 5.1.4 on 2025-02-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
