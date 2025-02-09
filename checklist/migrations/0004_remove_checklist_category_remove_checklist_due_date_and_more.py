# Generated by Django 5.1.4 on 2025-01-15 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0003_remove_checklist_entry_entry_checklist_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='category',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='entry',
        ),
        migrations.AddField(
            model_name='entry',
            name='checklist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checklist.checklist'),
        ),
        migrations.AddField(
            model_name='entry',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
