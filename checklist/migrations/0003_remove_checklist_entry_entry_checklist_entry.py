# Generated by Django 5.1.4 on 2025-01-14 20:50

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0002_checklist_category_checklist_due_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='entry',
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Add and entry to your list.', max_length=200, unique=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='entry_name_case_insensitive_unique', violation_error_message='Entry already exists (case insensitive match)')],
            },
        ),
        migrations.AddField(
            model_name='checklist',
            name='entry',
            field=models.ManyToManyField(help_text='Add an entry to your list.', to='checklist.entry'),
        ),
    ]
