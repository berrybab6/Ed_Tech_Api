# Generated by Django 3.1 on 2021-04-13 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='reply',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
