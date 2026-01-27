"""Invoicing views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer, InvoiceCreateSerializer
from sifen.services import SifenService


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
    def generate_cdc(self, request, pk=None):
        """Generar CDC y XML para la factura."""
        invoice = self.get_object()
        
        if invoice.status not in ['draft']:
            return Response(
                {'error': 'Solo se puede generar CDC para facturas en borrador'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = SifenService()
            result = service.generate_invoice(invoice)
            
            return Response({
                'success': True,
                'cdc': result['cdc'],
                'message': 'CDC y XML generados correctamente',
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def send_to_sifen(self, request, pk=None):
        """Enviar factura a SIFEN."""
        invoice = self.get_object()
        
        if invoice.status not in ['draft', 'pending', 'rejected']:
            return Response(
                {'error': 'La factura no puede ser enviada en este estado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = SifenService()
            
            # Generate CDC/XML if not already done
            if not invoice.cdc:
                service.generate_invoice(invoice)
                invoice.refresh_from_db()
            
            # Send to SIFEN
            result = service.send_to_sifen(invoice)
            
            return Response({
                'success': result['success'],
                'cdc': invoice.cdc,
                'response_code': result['response_code'],
                'message': result['response_message'],
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def xml(self, request, pk=None):
        """Obtener XML de la factura."""
        invoice = self.get_object()
        
        if not invoice.xml_signed:
            # Generate on the fly if possible
            if invoice.status == 'draft':
                try:
                    service = SifenService()
                    result = service.generate_invoice(invoice)
                    return Response({
                        'cdc': result['cdc'],
                        'xml': result['xml_signed']
                    })
                except Exception as e:
                    return Response(
                        {'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            return Response(
                {'error': 'XML no disponible'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'cdc': invoice.cdc,
            'xml': invoice.xml_signed
        })
