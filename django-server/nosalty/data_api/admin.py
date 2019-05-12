from django.contrib import admin
from .models import DataAggregator


class DataAggregatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'vacancy_name', 'company_name', 'city', 'category')
    readonly_fields = ('timestamp',)


admin.site.register(DataAggregator, DataAggregatorAdmin)