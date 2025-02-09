# Generated by Django 5.1.4 on 2025-01-28 19:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0008_remove_entry_entry_name_case_insensitive_unique_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='entry',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entry',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created'),
        ),
        migrations.AddField(
            model_name='entry',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='checklist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='checklist.checklist'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends_with', to='checklist.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='checklist',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='checklist.profile'),
        ),
    ]
