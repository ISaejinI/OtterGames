# Generated by Django 5.2.1 on 2025-05-25 16:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournois', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pari',
            name='pseudo',
        ),
        migrations.AddField(
            model_name='pari',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='userId', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
