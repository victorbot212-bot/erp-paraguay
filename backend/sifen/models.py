"""SIFEN models for audit and tracking."""
from django.db import models


class SifenLog(models.Model):
    """Log de comunicaciones con SIFEN."""
    
    ACTION_CHOICES = [
        ('send', 'Envío DE'),
        ('batch', 'Envío Lote'),
        ('query', 'Consulta'),
        ('cancel', 'Anulación'),
        ('event', 'Evento'),
    ]
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    cdc = models.CharField(max_length=44, blank=True, db_index=True)
    batch_id = models.CharField(max_length=50, blank=True)
    
    # Request/Response
    request_xml = models.TextField(blank=True)
    response_xml = models.TextField(blank=True)
    response_code = models.CharField(max_length=10)
    response_message = models.TextField(blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    duration_ms = models.PositiveIntegerField(null=True)
    
    class Meta:
        verbose_name = 'Log SIFEN'
        verbose_name_plural = 'Logs SIFEN'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action} - {self.response_code} - {self.created_at}"
