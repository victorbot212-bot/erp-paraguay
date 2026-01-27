"""SIFEN views."""
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .cdc import validate_cdc


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sifen_status(request):
    """Check SIFEN configuration status."""
    return Response({
        'environment': settings.SIFEN_ENVIRONMENT,
        'api_url': settings.SIFEN_API_URL,
        'certificate_configured': bool(settings.SIFEN_CERT_PATH),
        'status': 'configured' if settings.SIFEN_CERT_PATH else 'pending_certificate',
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_cdc_view(request, cdc: str):
    """Validate a CDC."""
    is_valid = validate_cdc(cdc)
    
    result = {
        'cdc': cdc,
        'valid': is_valid,
    }
    
    if is_valid:
        # Parse CDC components
        result['parsed'] = {
            'tipo_de': cdc[0:2],
            'ruc': f"{cdc[2:10]}-{cdc[10]}",
            'establecimiento': cdc[11:14],
            'punto': cdc[14:17],
            'numero': cdc[17:24],
            'tipo_contribuyente': cdc[24],
            'fecha_emision': f"{cdc[25:29]}-{cdc[29:31]}-{cdc[31:33]}",
            'tipo_emision': cdc[33],
            'codigo_seguridad': cdc[34:43],
            'dv': cdc[43],
        }
    
    return Response(result)
