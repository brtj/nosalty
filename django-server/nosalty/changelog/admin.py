from django.contrib import admin
from changelog.models import ChangeLog


class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('version', 'title', 'created_at')
    readonly_fields = ('timestamp',)
    ordering = ('-created_at',)


admin.site.register(ChangeLog, ChangeLogAdmin)
