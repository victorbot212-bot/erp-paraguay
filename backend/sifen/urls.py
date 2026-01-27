"""SIFEN URL configuration."""
from django.urls import path
from . import views, catalog_views

urlpatterns = [
    # Status and validation
    path('status/', views.sifen_status, name='sifen-status'),
    path('validate-cdc/<str:cdc>/', views.validate_cdc_view, name='validate-cdc'),
    
    # Catalogs
    path('catalogs/departamentos/', catalog_views.departamentos_list, name='departamentos-list'),
    path('catalogs/departamentos/<str:codigo>/', catalog_views.departamento_detail, name='departamento-detail'),
    path('catalogs/actividades/', catalog_views.actividades_list, name='actividades-list'),
    path('catalogs/actividades/search/', catalog_views.actividades_search, name='actividades-search'),
    path('catalogs/documentos/', catalog_views.tipos_documento_list, name='documentos-list'),
    path('catalogs/monedas/', catalog_views.monedas_list, name='monedas-list'),
    path('catalogs/iva/', catalog_views.tasas_iva_list, name='tasas-iva-list'),
    path('catalogs/unidades/', catalog_views.unidades_search, name='unidades-list'),
]
