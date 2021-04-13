from django.db import models
from django.conf import settings
# Create your models here.
class Comment(models.Model):
    comment = models.CharField(max_length=500)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comment", default=False, on_delete=models.CASCADE, null=True)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name="reply", on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)