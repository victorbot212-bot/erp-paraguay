"""Company models for ERP Paraguay."""
from django.db import models
from django.core.validators import RegexValidator


class Company(models.Model):
    """Empresa/Contribuyente."""
    
    ruc_validator = RegexValidator(
        regex=r'^\d{1,8}-\d$',
        message='RUC debe tener formato: 12345678-9'
    )
    
    # Identificación
    ruc = models.CharField(
        max_length=12,
        unique=True,
        validators=[ruc_validator],
        help_text='RUC con dígito verificador (ej: 80012345-6)'
    )
    razon_social = models.CharField(max_length=255)
    nombre_fantasia = models.CharField(max_length=255, blank=True)
    
    # Actividad económica (código DNIT)
    actividad_economica = models.CharField(max_length=10)
    
    # Ubicación
    departamento = models.CharField(max_length=50)
    distrito = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.TextField()
    
    # Contacto
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    
    # SIFEN
    timbrado = models.CharField(max_length=8, blank=True)
    fecha_inicio_timbrado = models.DateField(null=True, blank=True)
    fecha_fin_timbrado = models.DateField(null=True, blank=True)
    
    # Certificado digital
    certificado_path = models.CharField(max_length=500, blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['razon_social']
    
    def __str__(self):
        return f"{self.ruc} - {self.razon_social}"
    
    @property
    def ruc_sin_dv(self):
        """RUC sin dígito verificador."""
        return self.ruc.split('-')[0]
    
    @property
    def digito_verificador(self):
        """Dígito verificador del RUC."""
        return self.ruc.split('-')[1]


class EstablishmentPoint(models.Model):
    """Establecimiento y punto de expedición."""
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='establishments'
    )
    
    codigo_establecimiento = models.CharField(max_length=3)  # 001-999
    codigo_punto = models.CharField(max_length=3)  # 001-999
    descripcion = models.CharField(max_length=255)
    direccion = models.TextField(blank=True)
    
    # Numeración actual por tipo de documento
    # Se maneja en invoicing app
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'
        unique_together = ['company', 'codigo_establecimiento', 'codigo_punto']
        ordering = ['codigo_establecimiento', 'codigo_punto']
    
    def __str__(self):
        return f"{self.company.ruc} - {self.codigo_establecimiento}-{self.codigo_punto}"
