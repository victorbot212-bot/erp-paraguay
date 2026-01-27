"""URL configuration for ERP Paraguay."""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/companies/', include('companies.urls')),
    path('api/invoicing/', include('invoicing.urls')),
    path('api/sifen/', include('sifen.urls')),
]
