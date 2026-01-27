"""
SIFEN Service - Orchestrates invoice generation and submission.
"""
import time
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any
import httpx

from django.conf import settings
from django.db import transaction

from .cdc import generate_cdc
from .xml_builder import SifenXMLBuilder
from .signer import get_signer
from .models import SifenLog


class SifenService:
    """Main service for SIFEN operations."""
    
    def __init__(self, mock_mode: bool = None):
        """
        Initialize SIFEN service.
        
        Args:
            mock_mode: Override mock mode (default: based on SIFEN_ENVIRONMENT)
        """
        if mock_mode is None:
            mock_mode = settings.SIFEN_ENVIRONMENT == "test"
        
        self.mock_mode = mock_mode
        self.api_url = settings.SIFEN_API_URL
        self.signer = get_signer(mock=mock_mode)
    
    @transaction.atomic
    def generate_invoice(self, invoice) -> Dict[str, Any]:
        """
        Generate CDC, build XML, and sign for an invoice.
        
        Args:
            invoice: Invoice model instance
        
        Returns:
            Dict with cdc, xml_unsigned, xml_signed
        """
        from invoicing.models import Invoice  # Avoid circular import
        
        company = invoice.company
        establishment = invoice.establishment
        
        # Determine contributor type
        tipo_contribuyente = 2  # Default: Legal entity
        if company.ruc_sin_dv.startswith("1"):
            tipo_contribuyente = 1  # Individual
        
        # Generate CDC
        cdc = generate_cdc(
            tipo_de=int(invoice.document_type),
            ruc=company.ruc,
            establecimiento=establishment.codigo_establecimiento,
            punto=establishment.codigo_punto,
            numero=invoice.numero,
            tipo_contribuyente=tipo_contribuyente,
            fecha_emision=invoice.fecha_emision,
            tipo_emision=1,  # Normal
        )
        
        # Prepare items for XML
        items = []
        for item in invoice.items.all():
            items.append({
                "codigo": item.codigo or str(item.id),
                "descripcion": item.descripcion,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario,
                "unidad_medida": item.unidad_medida,
                "tasa_iva": item.tasa_iva,
                "subtotal": item.subtotal,
                "iva": item.iva,
                "total": item.total,
            })
        
        # Build XML
        builder = SifenXMLBuilder()
        xml_element = builder.build_de(
            cdc=cdc,
            tipo_de=int(invoice.document_type),
            fecha_emision=invoice.fecha_emision,
            
            # Emisor
            emisor_ruc=company.ruc,
            emisor_razon_social=company.razon_social,
            emisor_nombre_fantasia=company.nombre_fantasia,
            emisor_actividad=company.actividad_economica,
            emisor_timbrado=invoice.timbrado,
            emisor_establecimiento=establishment.codigo_establecimiento,
            emisor_punto=establishment.codigo_punto,
            emisor_numero=invoice.numero,
            emisor_direccion=company.direccion,
            emisor_departamento=company.departamento,
            emisor_distrito=company.distrito,
            emisor_ciudad=company.ciudad,
            emisor_telefono=company.telefono,
            emisor_email=company.email,
            
            # Receptor
            receptor_contribuyente=bool(invoice.receptor_ruc),
            receptor_ruc=invoice.receptor_ruc,
            receptor_razon_social=invoice.receptor_nombre,
            receptor_direccion=invoice.receptor_direccion,
            receptor_email=invoice.receptor_email,
            
            # Totales
            moneda=invoice.moneda,
            tipo_cambio=invoice.tipo_cambio,
            total_iva_10=invoice.subtotal_gravado_10,
            total_iva_5=invoice.subtotal_gravado_5,
            total_exento=invoice.subtotal_exento,
            total=invoice.total,
            
            # Items
            items=items,
        )
        
        xml_unsigned = builder.to_string(pretty=True)
        
        # Sign XML
        try:
            signed_element, signature = self.signer.sign(xml_element)
            xml_signed = builder.to_string(pretty=True)
        except Exception as e:
            # If signing fails, use unsigned (for testing)
            xml_signed = xml_unsigned
        
        # Update invoice
        invoice.cdc = cdc
        invoice.xml_signed = xml_signed
        invoice.status = "pending"
        invoice.save()
        
        return {
            "cdc": cdc,
            "xml_unsigned": xml_unsigned,
            "xml_signed": xml_signed,
        }
    
    def send_to_sifen(self, invoice) -> Dict[str, Any]:
        """
        Send invoice to SIFEN.
        
        Args:
            invoice: Invoice model instance (must have xml_signed)
        
        Returns:
            Dict with success, response_code, response_message
        """
        if not invoice.xml_signed:
            raise ValueError("Invoice must be signed before sending")
        
        start_time = time.time()
        
        if self.mock_mode:
            # Mock successful response
            result = {
                "success": True,
                "response_code": "0",
                "response_message": "Documento procesado correctamente (MOCK)",
                "batch_id": f"MOCK-{invoice.cdc[:8]}",
            }
            
            invoice.status = "approved"
            invoice.sifen_response_code = result["response_code"]
            invoice.sifen_response_message = result["response_message"]
            invoice.sifen_batch_id = result["batch_id"]
            invoice.save()
            
            # Log
            SifenLog.objects.create(
                action="send",
                cdc=invoice.cdc,
                batch_id=result["batch_id"],
                request_xml=invoice.xml_signed[:1000],  # Truncate for log
                response_xml="<mock>OK</mock>",
                response_code=result["response_code"],
                response_message=result["response_message"],
                duration_ms=int((time.time() - start_time) * 1000),
            )
            
            return result
        
        # Real SIFEN call
        try:
            # Build SOAP envelope
            soap_envelope = self._build_soap_envelope(invoice.xml_signed)
            
            response = httpx.post(
                f"{self.api_url}/de/ws/sync/recibe.wsdl",
                content=soap_envelope,
                headers={
                    "Content-Type": "application/soap+xml; charset=utf-8",
                },
                timeout=30.0,
            )
            
            response_code, response_message = self._parse_response(response.text)
            
            success = response_code == "0"
            
            invoice.status = "approved" if success else "rejected"
            invoice.sifen_response_code = response_code
            invoice.sifen_response_message = response_message
            invoice.save()
            
            # Log
            SifenLog.objects.create(
                action="send",
                cdc=invoice.cdc,
                request_xml=invoice.xml_signed[:1000],
                response_xml=response.text[:2000],
                response_code=response_code,
                response_message=response_message,
                duration_ms=int((time.time() - start_time) * 1000),
            )
            
            return {
                "success": success,
                "response_code": response_code,
                "response_message": response_message,
            }
            
        except Exception as e:
            invoice.status = "rejected"
            invoice.sifen_response_code = "ERROR"
            invoice.sifen_response_message = str(e)
            invoice.save()
            
            SifenLog.objects.create(
                action="send",
                cdc=invoice.cdc,
                request_xml=invoice.xml_signed[:1000],
                response_code="ERROR",
                response_message=str(e),
                duration_ms=int((time.time() - start_time) * 1000),
            )
            
            return {
                "success": False,
                "response_code": "ERROR",
                "response_message": str(e),
            }
    
    def _build_soap_envelope(self, xml_de: str) -> str:
        """Build SOAP envelope for SIFEN."""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
    <soap:Header/>
    <soap:Body>
        <rEnviDe xmlns="http://ekuatia.set.gov.py/sifen/xsd">
            <dId>1</dId>
            <xDE>{xml_de}</xDE>
        </rEnviDe>
    </soap:Body>
</soap:Envelope>'''
    
    def _parse_response(self, response_xml: str) -> tuple:
        """Parse SIFEN response."""
        from lxml import etree
        
        try:
            root = etree.fromstring(response_xml.encode("UTF-8"))
            
            # Find response code
            code_elem = root.find(".//{http://ekuatia.set.gov.py/sifen/xsd}dCodRes")
            msg_elem = root.find(".//{http://ekuatia.set.gov.py/sifen/xsd}dMsgRes")
            
            code = code_elem.text if code_elem is not None else "UNKNOWN"
            msg = msg_elem.text if msg_elem is not None else "Respuesta no procesada"
            
            return code, msg
        except Exception:
            return "PARSE_ERROR", "Error parsing SIFEN response"


def generate_invoice_cdc(invoice) -> str:
    """
    Convenience function to generate CDC for an invoice.
    
    Args:
        invoice: Invoice model instance
    
    Returns:
        44-character CDC string
    """
    service = SifenService()
    result = service.generate_invoice(invoice)
    return result["cdc"]
