from django.db import models
from django.conf import settings

# Create your models here.

def resource_directory_path(instance, filename):
    return 'resources/{0}/'.format(filename)
class Resources(models.Model):
    EXAMS = 1
    ASSIGNMENT = 2
    TUTORIALS = 3
    BOOKS = 4
    LECTURES = 5
    OTHER_TYPE = 6
    RESOURCE_TYPES = (
        (EXAMS, 'exams'),
        (BOOKS, 'books'),
        (LECTURES, 'lectures'),
        (TUTORIALS, 'tutorials'),
        (ASSIGNMENT, 'assignment'),
        (OTHER_TYPE, 'other')
    )

    SOFTWARE = 1
    MECHANICAL = 2
    CIVIL = 3
    CHEMICAL = 4
    ELECTRICAL = 5
    IT = 6
    OTHER = 8
    BIOMED = 7
    CATEGORY = (
        (SOFTWARE, "software"),
        (MECHANICAL, "mechanical"),
        (CIVIL, "civil"),
        (CHEMICAL, "chemical"),
        (ELECTRICAL, "electrical"),
        (IT, "it"),
        (BIOMED, "biomed"),
        (OTHER, "other")
    )
    resource_type = models.PositiveSmallIntegerField(choices=RESOURCE_TYPES, default=6)
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="resources" ,default=False, on_delete=models.CASCADE, null=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY, default=8)
    description = models.CharField(null=True, blank=True, max_length=255)
    resource_file = models.FileField(upload_to=resource_directory_path, null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now=True)
