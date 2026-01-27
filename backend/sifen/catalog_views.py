"""API views for SIFEN catalogs."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .catalogs import (
    DEPARTAMENTOS, get_departamento,
    ACTIVIDADES_ECONOMICAS, buscar_actividad,
    TIPOS_DOCUMENTO, MONEDAS, TASAS_IVA,
    UNIDADES_MEDIDA, buscar_unidad,
)
from .catalogs.documentos import TIPOS_DE, TIPO_OPERACION


@api_view(['GET'])
@permission_classes([AllowAny])
def departamentos_list(request):
    """List all departments."""
    result = []
    for codigo, data in DEPARTAMENTOS.items():
        result.append({
            "codigo": codigo,
            "nombre": data["nombre"],
            "distritos_count": len(data.get("distritos", {}))
        })
    return Response(sorted(result, key=lambda x: int(x["codigo"])))


@api_view(['GET'])
@permission_classes([AllowAny])
def departamento_detail(request, codigo):
    """Get department with districts."""
    data = get_departamento(codigo)
    distritos = [
        {"codigo": k, "nombre": v}
        for k, v in data.get("distritos", {}).items()
    ]
    return Response({
        "codigo": codigo,
        "nombre": data["nombre"],
        "distritos": sorted(distritos, key=lambda x: int(x["codigo"]))
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def actividades_search(request):
    """Search economic activities."""
    termino = request.GET.get('q', '')
    if len(termino) < 2:
        return Response([])
    
    resultados = buscar_actividad(termino)
    return Response(resultados)


@api_view(['GET'])
@permission_classes([AllowAny])
def actividades_list(request):
    """List economic activities (paginated)."""
    limit = int(request.GET.get('limit', 50))
    offset = int(request.GET.get('offset', 0))
    
    items = list(ACTIVIDADES_ECONOMICAS.items())[offset:offset+limit]
    result = [
        {"codigo": k, "descripcion": v}
        for k, v in items
    ]
    return Response({
        "count": len(ACTIVIDADES_ECONOMICAS),
        "results": result
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def tipos_documento_list(request):
    """List document types."""
    return Response({
        "tipos_de": [{"codigo": k, "descripcion": v} for k, v in TIPOS_DE.items()],
        "tipos_identidad": [{"codigo": k, "descripcion": v} for k, v in TIPOS_DOCUMENTO.items()],
        "tipos_operacion": [{"codigo": k, "descripcion": v} for k, v in TIPO_OPERACION.items()],
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def monedas_list(request):
    """List currencies."""
    result = [
        {
            "codigo": k,
            "nombre": v["nombre"],
            "simbolo": v["simbolo"],
            "decimales": v["decimales"]
        }
        for k, v in MONEDAS.items()
    ]
    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def tasas_iva_list(request):
    """List IVA rates."""
    result = [
        {
            "tasa": k,
            "descripcion": v["descripcion"],
            "codigo_afectacion": v["codigo_afectacion"],
        }
        for k, v in TASAS_IVA.items()
    ]
    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def unidades_search(request):
    """Search units of measure."""
    termino = request.GET.get('q', '')
    if termino:
        resultados = buscar_unidad(termino)
    else:
        resultados = [
            {"codigo_sifen": k, "codigo": v["codigo"], "descripcion": v["descripcion"]}
            for k, v in UNIDADES_MEDIDA.items()
        ]
    return Response(resultados)
