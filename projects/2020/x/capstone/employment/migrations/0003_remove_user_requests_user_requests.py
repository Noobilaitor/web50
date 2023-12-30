# Generated by Django 4.0.3 on 2023-12-29 19:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0002_alter_user_requests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='requests',
        ),
        migrations.AddField(
            model_name='user',
            name='requests',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]