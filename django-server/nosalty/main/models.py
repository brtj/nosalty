from django.db import models

# Create your models here.

class ChangeLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    version = models.CharField(max_length=250)
    message = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    salary_uop_min = models.IntegerField(null=True)
    salary_uop_max = models.IntegerField(null=True)
    salary_b2b_min = models.IntegerField(null=True)
    salary_b2b_max = models.IntegerField(null=True)
    url_to_offer = models.URLField(max_length=250)