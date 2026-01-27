"""Invoicing models for ERP Paraguay."""
from django.db import models
from companies.models import Company, EstablishmentPoint


class DocumentType(models.TextChoices):
    """Tipos de documentos electrónicos SIFEN."""
    FACTURA_ELECTRONICA = '1', 'Factura Electrónica'
    FACTURA_ELECTRONICA_EXPORTACION = '2', 'Factura Electrónica de Exportación'
    FACTURA_ELECTRONICA_IMPORTACION = '3', 'Factura Electrónica de Importación'
    AUTOFACTURA_ELECTRONICA = '4', 'Autofactura Electrónica'
    NOTA_CREDITO_ELECTRONICA = '5', 'Nota de Crédito Electrónica'
    NOTA_DEBITO_ELECTRONICA = '6', 'Nota de Débito Electrónica'
    NOTA_REMISION_ELECTRONICA = '7', 'Nota de Remisión Electrónica'


class InvoiceStatus(models.TextChoices):
    """Estados del documento electrónico."""
    DRAFT = 'draft', 'Borrador'
    PENDING = 'pending', 'Pendiente de envío'
    SENT = 'sent', 'Enviado a SIFEN'
    APPROVED = 'approved', 'Aprobado'
    REJECTED = 'rejected', 'Rechazado'
    CANCELLED = 'cancelled', 'Anulado'


class Invoice(models.Model):
    """Documento electrónico (Factura, Nota de Crédito, etc.)."""
    
    # Emisor
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    establishment = models.ForeignKey(
        EstablishmentPoint,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    
    # Tipo y numeración
    document_type = models.CharField(
        max_length=2,
        choices=DocumentType.choices,
        default=DocumentType.FACTURA_ELECTRONICA
    )
    numero = models.PositiveIntegerField()  # 0000001-9999999
    
    # CDC (Código de Control) - 44 caracteres
    cdc = models.CharField(max_length=44, unique=True, blank=True)
    
    # Timbrado
    timbrado = models.CharField(max_length=8)
    
    # Receptor
    receptor_ruc = models.CharField(max_length=12, blank=True)
    receptor_nombre = models.CharField(max_length=255)
    receptor_direccion = models.TextField(blank=True)
    receptor_email = models.EmailField(blank=True)
    
    # Fechas
    fecha_emision = models.DateTimeField()
    
    # Moneda y tipo de cambio
    moneda = models.CharField(max_length=3, default='PYG')  # ISO 4217
    tipo_cambio = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=1
    )
    
    # Totales
    subtotal_gravado_10 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    subtotal_gravado_5 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    subtotal_exento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_iva_10 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_iva_5 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Estado SIFEN
    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT
    )
    sifen_response_code = models.CharField(max_length=10, blank=True)
    sifen_response_message = models.TextField(blank=True)
    sifen_batch_id = models.CharField(max_length=50, blank=True)
    
    # XML firmado
    xml_signed = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']
        unique_together = ['company', 'establishment', 'document_type', 'numero']
    
    def __str__(self):
        return f"{self.get_document_type_display()} {self.numero_completo}"
    
    @property
    def numero_completo(self):
        """Número completo: establecimiento-punto-numero."""
        return (
            f"{self.establishment.codigo_establecimiento}-"
            f"{self.establishment.codigo_punto}-"
            f"{str(self.numero).zfill(7)}"
        )


class InvoiceItem(models.Model):
    """Línea/ítem de factura."""
    
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    # Producto/Servicio
    codigo = models.CharField(max_length=50, blank=True)
    descripcion = models.CharField(max_length=500)
    unidad_medida = models.CharField(max_length=10, default='UNI')
    
    # Cantidades y precios
    cantidad = models.DecimalField(max_digits=15, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=4)
    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # IVA: 10%, 5%, 0%
    tasa_iva = models.IntegerField(
        choices=[(10, '10%'), (5, '5%'), (0, 'Exento')],
        default=10
    )
    
    # Calculados
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    iva = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        verbose_name = 'Ítem de Factura'
        verbose_name_plural = 'Ítems de Factura'
        ordering = ['id']
    
    def __str__(self):
        return f"{self.descripcion} x {self.cantidad}"
    
    def save(self, *args, **kwargs):
        """Calcular totales antes de guardar."""
        self.subtotal = (self.cantidad * self.precio_unitario) - self.descuento
        if self.tasa_iva > 0:
            # IVA incluido en Paraguay
            self.iva = self.subtotal - (self.subtotal / (1 + self.tasa_iva / 100))
        else:
            self.iva = 0
        self.total = self.subtotal
        super().save(*args, **kwargs)
