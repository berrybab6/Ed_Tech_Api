# Generated by Django 3.1 on 2021-03-18 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210318_2230'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Roles',
            new_name='Role',
        ),
    ]
