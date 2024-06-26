# Generated by Django 5.0.4 on 2024-04-20 09:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_messagegroup_is_read'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagegroup',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='messagegroup',
            name='sub_message',
        ),
        migrations.AddField(
            model_name='messagegroup',
            name='users_read',
            field=models.ManyToManyField(related_name='users_read_group', to=settings.AUTH_USER_MODEL),
        ),
    ]
