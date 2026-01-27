"""Companies URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('companies', views.CompanyViewSet)
router.register('establishments', views.EstablishmentPointViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
