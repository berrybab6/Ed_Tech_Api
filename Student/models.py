from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(blank=True, null=True, max_length=150)
    head = models.CharField(blank=True, null=True, max_length=150)