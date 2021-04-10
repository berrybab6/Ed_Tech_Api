from django.db import models
from django.conf import settings

# Create your models here.
class Courses(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ETSC = models.PositiveIntegerField(null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="courses", default=False, on_delete=models.CASCADE, null=True)
