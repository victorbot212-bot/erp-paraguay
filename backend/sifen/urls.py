"""SIFEN URL configuration."""
from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.sifen_status, name='sifen-status'),
    path('validate-cdc/<str:cdc>/', views.validate_cdc_view, name='validate-cdc'),
]
