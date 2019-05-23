from django.contrib import admin
from .models import DataAggregator


class DataAggregatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'vacancy_name', 'company_name', 'city', 'category')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    list_filter = (
        'city',
        'category',
    )
    list_per_page = 200


admin.site.register(DataAggregator, DataAggregatorAdmin)