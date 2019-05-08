from django.db import models

# Create your models here.
class Nofluff_data(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    vacancy_name = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    salary_uop_min = models.IntegerField(null=True)
    salary_uop_max = models.IntegerField(null=True)
    salary_b2b_min = models.IntegerField(null=True)
    salary_b2b_max = models.IntegerField(null=True)
    url_to_offer = models.URLField(max_length=250)

    def __str__(self):
        return self.company_name