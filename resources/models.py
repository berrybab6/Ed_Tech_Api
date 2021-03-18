from django.db import models

# Create your models here.
class Resources(models.Model):
    EXAMS = 1
    ASSIGNMENT = 2
    TUTORIALS = 3
    BOOKS = 4
    LECTURES = 5

    RESOURCE_TYPES = (
        (EXAMS, 'exams'),
        (BOOKS, 'books'),
        (LECTURES, 'lectures'),
        (TUTORIALS, 'tutorials'),
        (ASSIGNMENT, 'assignment'),
    )

    SOFTWARE = 1
    MECHANICAL = 2
    CIVIL = 3
    CHEMICAL = 4
    ELECTRICAL =5 
    IT = 6
    BIOMED = 7
    CATEGORY = (
        (SOFTWARE, "software"),
        (MECHANICAL, "mechanical"),
        (CIVIL, "civil"),
        (CHEMICAL, "chemical"),
        (ELECTRICAL, "electrical"),
        (IT, "it"),
        (BIOMED, "biomed")
    )
    resource_type = models.PositiveSmallIntegerField(choices=RESOURCE_TYPES)
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY)