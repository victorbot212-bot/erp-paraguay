"""
Catálogo de Tipos de Documentos SIFEN.
"""

# Tipos de Documentos Electrónicos
TIPOS_DE = {
    "1": "Factura electrónica",
    "2": "Factura electrónica de exportación",
    "3": "Factura electrónica de importación",
    "4": "Autofactura electrónica",
    "5": "Nota de crédito electrónica",
    "6": "Nota de débito electrónica",
    "7": "Nota de remisión electrónica",
}

# Tipos de Documento de Identidad del Receptor
TIPOS_DOCUMENTO = {
    "1": "Cédula de Identidad",
    "2": "Pasaporte",
    "3": "Carnet de Residencia",
    "4": "Innominado",
    "5": "Tarjeta Diplomática de Exoneración Fiscal",
    "6": "Otros",
}

# Naturaleza del Receptor
NATURALEZA_RECEPTOR = {
    "1": "Contribuyente",
    "2": "No Contribuyente",
}

# Tipo de Operación
TIPO_OPERACION = {
    "1": "B2B",  # Business to Business
    "2": "B2C",  # Business to Consumer
    "3": "B2G",  # Business to Government
    "4": "B2F",  # Business to Foreign
}

# Tipo de Emisión
TIPO_EMISION = {
    "1": "Normal",
    "2": "Contingencia",
}

# Indicador de Presencia
INDICADOR_PRESENCIA = {
    "1": "Operación presencial",
    "2": "Operación electrónica",
    "3": "Operación por call center",
    "4": "Venta a domicilio",
    "5": "Operación bancaria",
    "6": "Operación cíclica",
    "9": "Otro",
}

# Tipo de Transacción
TIPO_TRANSACCION = {
    "1": "Venta de mercadería",
    "2": "Prestación de servicios",
    "3": "Mixto",
    "4": "Venta de activo fijo",
    "5": "Venta de divisas",
    "6": "Compra de divisas",
    "7": "Promoción o entrega de muestras",
    "8": "Donación",
    "9": "Anticipo",
    "10": "Compra de productos",
    "11": "Compra de servicios",
    "12": "Venta de crédito fiscal",
    "13": "Muestras médicas",
}


def get_tipo_documento(codigo: str) -> str:
    """Get document type description."""
    return TIPOS_DOCUMENTO.get(str(codigo), "Tipo desconocido")


def get_tipo_de(codigo: str) -> str:
    """Get electronic document type description."""
    return TIPOS_DE.get(str(codigo), "Tipo DE desconocido")


def get_tipo_operacion(codigo: str) -> str:
    """Get operation type description."""
    return TIPO_OPERACION.get(str(codigo), "Operación desconocida")
