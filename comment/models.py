from django.db import models
from django.conf import settings
from resources.models import Resources
# Create your models here.
class Comment(models.Model):
    resource = models.ForeignKey(Resources, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comment", null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comment", default=False, on_delete=models.CASCADE, null=True)

class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reply", null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="reply", on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    reply = models.CharField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True, blank=True, null=True)