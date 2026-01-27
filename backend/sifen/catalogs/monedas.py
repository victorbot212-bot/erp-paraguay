"""
Catálogo de Monedas (ISO 4217).
"""

MONEDAS = {
    "PYG": {"nombre": "Guaraní", "simbolo": "₲", "decimales": 0},
    "USD": {"nombre": "Dólar estadounidense", "simbolo": "$", "decimales": 2},
    "EUR": {"nombre": "Euro", "simbolo": "€", "decimales": 2},
    "BRL": {"nombre": "Real brasileño", "simbolo": "R$", "decimales": 2},
    "ARS": {"nombre": "Peso argentino", "simbolo": "$", "decimales": 2},
    "UYU": {"nombre": "Peso uruguayo", "simbolo": "$U", "decimales": 2},
    "CLP": {"nombre": "Peso chileno", "simbolo": "$", "decimales": 0},
    "BOB": {"nombre": "Boliviano", "simbolo": "Bs", "decimales": 2},
    "PEN": {"nombre": "Sol peruano", "simbolo": "S/", "decimales": 2},
    "COP": {"nombre": "Peso colombiano", "simbolo": "$", "decimales": 2},
    "GBP": {"nombre": "Libra esterlina", "simbolo": "£", "decimales": 2},
    "JPY": {"nombre": "Yen japonés", "simbolo": "¥", "decimales": 0},
    "CNY": {"nombre": "Yuan chino", "simbolo": "¥", "decimales": 2},
    "CHF": {"nombre": "Franco suizo", "simbolo": "CHF", "decimales": 2},
    "CAD": {"nombre": "Dólar canadiense", "simbolo": "C$", "decimales": 2},
    "AUD": {"nombre": "Dólar australiano", "simbolo": "A$", "decimales": 2},
    "MXN": {"nombre": "Peso mexicano", "simbolo": "$", "decimales": 2},
}


def get_moneda(codigo: str) -> dict:
    """Get currency info by ISO code."""
    return MONEDAS.get(codigo.upper(), {
        "nombre": "Moneda desconocida",
        "simbolo": codigo,
        "decimales": 2
    })


def format_moneda(valor: float, codigo: str = "PYG") -> str:
    """Format a value with currency symbol."""
    moneda = get_moneda(codigo)
    decimales = moneda["decimales"]
    simbolo = moneda["simbolo"]
    
    if decimales == 0:
        return f"{simbolo} {int(valor):,}"
    return f"{simbolo} {valor:,.{decimales}f}"
