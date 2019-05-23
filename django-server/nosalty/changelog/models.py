from django.db import models

# Create your models here.
class ChangeLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    version = models.CharField(max_length=250)
    message = models.TextField(max_length=250)
    tag_name = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    published_at = models.DateTimeField()