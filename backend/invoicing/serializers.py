"""Invoicing serializers."""
from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ['subtotal', 'iva', 'total']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    numero_completo = serializers.ReadOnlyField()
    document_type_display = serializers.CharField(
        source='get_document_type_display',
        read_only=True
    )
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['cdc', 'xml_signed', 'sifen_response_code', 'sifen_response_message']


class InvoiceCreateSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    
    class Meta:
        model = Invoice
        exclude = ['cdc', 'xml_signed', 'status']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        
        # Calcular totales
        invoice.subtotal_gravado_10 = sum(
            i.subtotal for i in invoice.items.filter(tasa_iva=10)
        )
        invoice.subtotal_gravado_5 = sum(
            i.subtotal for i in invoice.items.filter(tasa_iva=5)
        )
        invoice.subtotal_exento = sum(
            i.subtotal for i in invoice.items.filter(tasa_iva=0)
        )
        invoice.total_iva_10 = sum(
            i.iva for i in invoice.items.filter(tasa_iva=10)
        )
        invoice.total_iva_5 = sum(
            i.iva for i in invoice.items.filter(tasa_iva=5)
        )
        invoice.total = sum(i.total for i in invoice.items.all())
        invoice.save()
        
        return invoice
