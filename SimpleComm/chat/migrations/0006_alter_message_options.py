# Generated by Django 5.1.6 on 2025-03-09 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_user_room'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['createdAt']},
        ),
    ]
