# Generated by Django 5.1.4 on 2025-01-20 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0006_checklist_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='checklist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.checklist'),
        ),
    ]