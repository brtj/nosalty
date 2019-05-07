from django.contrib import admin
from .models import Nofluff_data


class Nofluff_dataAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'vacancy_name', 'company_name', 'city', 'category')
    readonly_fields = ('timestamp',)


admin.site.register(Nofluff_data, Nofluff_dataAdmin)