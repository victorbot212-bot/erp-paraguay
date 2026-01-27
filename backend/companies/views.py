"""Companies views."""
from rest_framework import viewsets
from .models import Company, EstablishmentPoint
from .serializers import CompanySerializer, EstablishmentPointSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """CRUD para empresas."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_fields = ['is_active', 'departamento']
    search_fields = ['ruc', 'razon_social', 'nombre_fantasia']


class EstablishmentPointViewSet(viewsets.ModelViewSet):
    """CRUD para establecimientos."""
    queryset = EstablishmentPoint.objects.all()
    serializer_class = EstablishmentPointSerializer
    filterset_fields = ['company', 'is_active']
