"""
Catálogo de Tasas de IVA Paraguay.
"""

TASAS_IVA = {
    10: {
        "descripcion": "IVA 10%",
        "codigo_afectacion": "1",
        "descripcion_afectacion": "Gravado IVA",
    },
    5: {
        "descripcion": "IVA 5%",
        "codigo_afectacion": "1",
        "descripcion_afectacion": "Gravado IVA",
    },
    0: {
        "descripcion": "Exento",
        "codigo_afectacion": "3",
        "descripcion_afectacion": "Exento",
    },
}

# Afectación IVA
AFECTACION_IVA = {
    "1": "Gravado IVA",
    "2": "Exonerado",
    "3": "Exento",
    "4": "Gravado parcial",
}

# Tipo de Impuesto
TIPO_IMPUESTO = {
    "1": "IVA",
    "2": "ISC",
    "3": "Renta",
    "4": "Ninguno",
    "5": "IVA - Renta",
}


def get_tasa_iva(tasa: int) -> dict:
    """Get IVA rate info."""
    return TASAS_IVA.get(tasa, TASAS_IVA[10])


def calcular_iva(base_con_iva: float, tasa: int) -> dict:
    """
    Calculate IVA from base amount (IVA included).
    
    In Paraguay, prices typically include IVA.
    
    Args:
        base_con_iva: Amount with IVA included
        tasa: IVA rate (10, 5, or 0)
    
    Returns:
        Dict with base_sin_iva, iva, total
    """
    if tasa == 0:
        return {
            "base_sin_iva": base_con_iva,
            "iva": 0,
            "total": base_con_iva,
        }
    
    divisor = 1 + (tasa / 100)
    base_sin_iva = base_con_iva / divisor
    iva = base_con_iva - base_sin_iva
    
    return {
        "base_sin_iva": round(base_sin_iva, 2),
        "iva": round(iva, 2),
        "total": base_con_iva,
    }


def calcular_iva_desde_base(base_sin_iva: float, tasa: int) -> dict:
    """
    Calculate IVA from base amount (without IVA).
    
    Args:
        base_sin_iva: Amount without IVA
        tasa: IVA rate (10, 5, or 0)
    
    Returns:
        Dict with base_sin_iva, iva, total
    """
    if tasa == 0:
        return {
            "base_sin_iva": base_sin_iva,
            "iva": 0,
            "total": base_sin_iva,
        }
    
    iva = base_sin_iva * (tasa / 100)
    total = base_sin_iva + iva
    
    return {
        "base_sin_iva": base_sin_iva,
        "iva": round(iva, 2),
        "total": round(total, 2),
    }
