"""
Catálogo de Unidades de Medida SIFEN.
"""

UNIDADES_MEDIDA = {
    "77": {"codigo": "UNI", "descripcion": "Unidad"},
    "83": {"codigo": "KG", "descripcion": "Kilogramo"},
    "21": {"codigo": "LT", "descripcion": "Litro"},
    "11": {"codigo": "M", "descripcion": "Metro"},
    "12": {"codigo": "M2", "descripcion": "Metro cuadrado"},
    "13": {"codigo": "M3", "descripcion": "Metro cúbico"},
    "14": {"codigo": "GLN", "descripcion": "Galón"},
    "18": {"codigo": "GRM", "descripcion": "Gramo"},
    "20": {"codigo": "CM", "descripcion": "Centímetro"},
    "23": {"codigo": "MM", "descripcion": "Milímetro"},
    "24": {"codigo": "PULG", "descripcion": "Pulgada"},
    "25": {"codigo": "PIE", "descripcion": "Pie"},
    "26": {"codigo": "YRD", "descripcion": "Yarda"},
    "27": {"codigo": "KM", "descripcion": "Kilómetro"},
    "28": {"codigo": "MG", "descripcion": "Miligramo"},
    "29": {"codigo": "ML", "descripcion": "Mililitro"},
    "30": {"codigo": "OZ", "descripcion": "Onza"},
    "31": {"codigo": "LB", "descripcion": "Libra"},
    "32": {"codigo": "TN", "descripcion": "Tonelada"},
    "33": {"codigo": "DOC", "descripcion": "Docena"},
    "34": {"codigo": "PAR", "descripcion": "Par"},
    "35": {"codigo": "CAJ", "descripcion": "Caja"},
    "36": {"codigo": "PAQ", "descripcion": "Paquete"},
    "37": {"codigo": "FAR", "descripcion": "Fardo"},
    "38": {"codigo": "BOL", "descripcion": "Bolsa"},
    "39": {"codigo": "ROL", "descripcion": "Rollo"},
    "40": {"codigo": "BID", "descripcion": "Bidón"},
    "41": {"codigo": "BOT", "descripcion": "Botella"},
    "42": {"codigo": "LAT", "descripcion": "Lata"},
    "43": {"codigo": "BLS", "descripcion": "Bolsón"},
    "44": {"codigo": "TAR", "descripcion": "Tarrina"},
    "45": {"codigo": "CIL", "descripcion": "Cilindro"},
    "46": {"codigo": "BAR", "descripcion": "Barril"},
    "47": {"codigo": "GAR", "descripcion": "Garrafa"},
    "48": {"codigo": "SOR", "descripcion": "Sobre"},
    "49": {"codigo": "TAB", "descripcion": "Tabla"},
    "50": {"codigo": "PZA", "descripcion": "Pieza"},
    "51": {"codigo": "JGO", "descripcion": "Juego"},
    "52": {"codigo": "SET", "descripcion": "Set"},
    "53": {"codigo": "KIT", "descripcion": "Kit"},
    "54": {"codigo": "HRS", "descripcion": "Hora"},
    "55": {"codigo": "DIA", "descripcion": "Día"},
    "56": {"codigo": "SEM", "descripcion": "Semana"},
    "57": {"codigo": "MES", "descripcion": "Mes"},
    "58": {"codigo": "AÑO", "descripcion": "Año"},
    "59": {"codigo": "MIN", "descripcion": "Minuto"},
    "60": {"codigo": "SEG", "descripcion": "Segundo"},
    "61": {"codigo": "SRV", "descripcion": "Servicio"},
    "99": {"codigo": "OTR", "descripcion": "Otro"},
}


def get_unidad_medida(codigo_sifen: str) -> dict:
    """Get unit of measure by SIFEN code."""
    return UNIDADES_MEDIDA.get(str(codigo_sifen), {
        "codigo": "UNI",
        "descripcion": "Unidad"
    })


def get_codigo_sifen(codigo_corto: str) -> str:
    """Get SIFEN code from short code (e.g., 'KG' -> '83')."""
    codigo_upper = codigo_corto.upper()
    for sifen_code, data in UNIDADES_MEDIDA.items():
        if data["codigo"] == codigo_upper:
            return sifen_code
    return "77"  # Default: Unidad


def buscar_unidad(termino: str) -> list:
    """Search units by term."""
    termino_lower = termino.lower()
    resultados = []
    for codigo, data in UNIDADES_MEDIDA.items():
        if (termino_lower in data["codigo"].lower() or 
            termino_lower in data["descripcion"].lower()):
            resultados.append({
                "codigo_sifen": codigo,
                "codigo": data["codigo"],
                "descripcion": data["descripcion"]
            })
    return resultados
