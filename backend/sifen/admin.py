"""SIFEN admin."""
from django.contrib import admin
from .models import SifenLog


@admin.register(SifenLog)
class SifenLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'cdc', 'response_code', 'duration_ms', 'created_at']
    list_filter = ['action', 'response_code']
    search_fields = ['cdc', 'batch_id']
    readonly_fields = ['request_xml', 'response_xml']
    date_hierarchy = 'created_at'
