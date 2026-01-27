"""Companies serializers."""
from rest_framework import serializers
from .models import Company, EstablishmentPoint


class EstablishmentPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentPoint
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    establishments = EstablishmentPointSerializer(many=True, read_only=True)
    
    class Meta:
        model = Company
        fields = '__all__'
