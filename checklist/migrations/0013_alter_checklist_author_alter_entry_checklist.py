# Generated by Django 5.1.4 on 2025-01-29 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0012_alter_checklist_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='checklist.profile'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='checklist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checklist.checklist'),
        ),
    ]
