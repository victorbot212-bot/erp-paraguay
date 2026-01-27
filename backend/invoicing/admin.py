"""Invoicing admin."""
from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ['subtotal', 'iva', 'total']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['numero_completo', 'company', 'receptor_nombre', 'total', 'status', 'fecha_emision']
    list_filter = ['status', 'document_type', 'company']
    search_fields = ['numero', 'cdc', 'receptor_nombre', 'receptor_ruc']
    readonly_fields = ['cdc', 'xml_signed']
    inlines = [InvoiceItemInline]
    date_hierarchy = 'fecha_emision'
