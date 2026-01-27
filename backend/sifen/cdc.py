"""
CDC (Código de Control Documentario) generator for SIFEN.
44 characters total.

Structure:
- Tipo DE (2): 01-07
- RUC Emisor (8): sin DV
- DV Emisor (1)
- Establecimiento (3): 001-999
- Punto Expedición (3): 001-999
- Número DE (7): 0000001-9999999
- Tipo Contribuyente (1): 1=Persona Física, 2=Persona Jurídica
- Fecha Emisión (8): YYYYMMDD
- Tipo Emisión (1): 1=Normal, 2=Contingencia
- Código Seguridad (9): aleatorio
- Dígito Verificador (1): módulo 11
"""
import secrets
from datetime import datetime


def calculate_check_digit(code: str) -> int:
    """
    Calculate check digit using módulo 11.
    Based on SIFEN Manual Técnico.
    """
    weights = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2]
    
    total = 0
    for i, char in enumerate(reversed(code)):
        total += int(char) * weights[i]
    
    remainder = total % 11
    
    if remainder == 0:
        return 0
    elif remainder == 1:
        return 0  # Special case per SIFEN spec
    else:
        return 11 - remainder


def generate_cdc(
    tipo_de: int,
    ruc: str,
    establecimiento: str,
    punto: str,
    numero: int,
    tipo_contribuyente: int,
    fecha_emision: datetime,
    tipo_emision: int = 1,
) -> str:
    """
    Generate a CDC (Código de Control Documentario).
    
    Args:
        tipo_de: Document type (1-7)
        ruc: RUC with check digit (e.g., "80012345-6")
        establecimiento: Establishment code (e.g., "001")
        punto: Point of sale code (e.g., "001")
        numero: Document number (1-9999999)
        tipo_contribuyente: 1=Individual, 2=Legal entity
        fecha_emision: Emission date
        tipo_emision: 1=Normal, 2=Contingency
    
    Returns:
        44-character CDC string
    """
    # Parse RUC
    ruc_parts = ruc.split('-')
    ruc_number = ruc_parts[0].zfill(8)
    ruc_dv = ruc_parts[1]
    
    # Format components
    tipo_de_str = str(tipo_de).zfill(2)
    numero_str = str(numero).zfill(7)
    tipo_contrib_str = str(tipo_contribuyente)
    fecha_str = fecha_emision.strftime('%Y%m%d')
    tipo_emision_str = str(tipo_emision)
    
    # Generate cryptographically secure random code
    codigo_seguridad = str(secrets.randbelow(1_000_000_000)).zfill(9)
    
    # Build CDC without check digit (43 chars)
    cdc_base = (
        f"{tipo_de_str}"      # 2: Tipo DE
        f"{ruc_number}"       # 8: RUC sin DV
        f"{ruc_dv}"           # 1: DV RUC
        f"{establecimiento}"  # 3: Establecimiento
        f"{punto}"            # 3: Punto
        f"{numero_str}"       # 7: Número
        f"{tipo_contrib_str}" # 1: Tipo Contribuyente
        f"{fecha_str}"        # 8: Fecha YYYYMMDD
        f"{tipo_emision_str}" # 1: Tipo Emisión
        f"{codigo_seguridad}" # 9: Código Seguridad
    )
    
    # Calculate check digit
    dv = calculate_check_digit(cdc_base)
    
    return f"{cdc_base}{dv}"


def validate_cdc(cdc: str) -> bool:
    """Validate a CDC's check digit."""
    if len(cdc) != 44:
        return False
    
    if not cdc.isdigit():
        return False
    
    base = cdc[:43]
    provided_dv = int(cdc[43])
    calculated_dv = calculate_check_digit(base)
    
    return provided_dv == calculated_dv
