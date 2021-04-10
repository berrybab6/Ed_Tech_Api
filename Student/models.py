from django.db import models
from django.conf import settings
from courses.models import Courses

# Create your models here.

class Student(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="course", default=False, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Courses, related_name="student_course", default=False, on_delete=models.CASCADE, null=True)

