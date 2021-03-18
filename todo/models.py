from django.db import models

# Create your models here.
class TODO(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
