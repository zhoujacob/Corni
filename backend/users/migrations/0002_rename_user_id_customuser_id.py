# Generated by Django 5.2.1 on 2025-06-21 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='user_id',
            new_name='id',
        ),
    ]
