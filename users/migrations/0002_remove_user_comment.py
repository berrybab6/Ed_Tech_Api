# Generated by Django 3.1 on 2021-04-14 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='comment',
        ),
    ]
