"""Companies admin."""
from django.contrib import admin
from .models import Company, EstablishmentPoint


class EstablishmentInline(admin.TabularInline):
    model = EstablishmentPoint
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['ruc', 'razon_social', 'is_active', 'created_at']
    list_filter = ['is_active', 'departamento']
    search_fields = ['ruc', 'razon_social']
    inlines = [EstablishmentInline]


@admin.register(EstablishmentPoint)
class EstablishmentPointAdmin(admin.ModelAdmin):
    list_display = ['company', 'codigo_establecimiento', 'codigo_punto', 'is_active']
    list_filter = ['is_active', 'company']
