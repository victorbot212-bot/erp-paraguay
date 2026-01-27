"""Invoicing views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer, InvoiceCreateSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """CRUD para facturas."""
    queryset = Invoice.objects.prefetch_related('items').all()
    filterset_fields = ['company', 'status', 'document_type']
    search_fields = ['numero', 'cdc', 'receptor_nombre', 'receptor_ruc']
    ordering_fields = ['fecha_emision', 'numero', 'total']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceCreateSerializer
        return InvoiceSerializer
    
    @action(detail=True, methods=['post'])
    def send_to_sifen(self, request, pk=None):
        """Enviar factura a SIFEN."""
        invoice = self.get_object()
        
        if invoice.status not in ['draft', 'pending', 'rejected']:
            return Response(
                {'error': 'La factura no puede ser enviada en este estado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implementar envío real a SIFEN
        # from sifen.services import SifenService
        # result = SifenService().send_invoice(invoice)
        
        return Response({
            'message': 'Factura enviada a SIFEN',
            'invoice_id': invoice.id,
            'cdc': invoice.cdc,
        })
    
    @action(detail=True, methods=['get'])
    def xml(self, request, pk=None):
        """Obtener XML de la factura."""
        invoice = self.get_object()
        
        if not invoice.xml_signed:
            return Response(
                {'error': 'XML no disponible'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'xml': invoice.xml_signed
        })
