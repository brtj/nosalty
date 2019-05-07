from django.contrib import admin
from .models import Nofluff_data


class Nofluff_dataAdmin(admin.ModelAdmin):
    list_display = ('id', 'vacancy_name', 'company_name', 'city', 'category')


admin.site.register(Nofluff_data, Nofluff_dataAdmin)