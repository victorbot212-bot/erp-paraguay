"""
SOAP Client for SIFEN Web Services.

Endpoints (Manual Técnico v150):
- /de/ws/sync/recibe.wsdl - Recepción síncrona de DE
- /de/ws/consulta/ruc.wsdl - Consulta RUC
- /de/ws/consulta/cdc.wsdl - Consulta por CDC
- /de/ws/evento/anulacion.wsdl - Anulación de DE
"""
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from lxml import etree
import httpx

from django.conf import settings
from .models import SifenLog


@dataclass
class SifenResponse:
    """Response from SIFEN web service."""
    success: bool
    response_code: str
    response_message: str
    raw_xml: str
    duration_ms: int
    data: Optional[Dict[str, Any]] = None


class SifenSoapClient:
    """
    SOAP client for SIFEN web services.
    
    Usage:
        client = SifenSoapClient()
        
        # Send document
        response = client.send_de(xml_signed)
        
        # Query by CDC
        response = client.query_cdc("01800123456001001...")
    """
    
    # SOAP envelope template
    SOAP_ENVELOPE = '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soap:Header/>
    <soap:Body>
        {body}
    </soap:Body>
</soap:Envelope>'''
    
    # SIFEN namespace
    NS = "http://ekuatia.set.gov.py/sifen/xsd"
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize SOAP client.
        
        Args:
            base_url: SIFEN API base URL (default from settings)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or settings.SIFEN_API_URL
        self.timeout = timeout
        self.environment = settings.SIFEN_ENVIRONMENT
    
    def _build_soap_request(self, body: str) -> str:
        """Build complete SOAP envelope."""
        return self.SOAP_ENVELOPE.format(body=body)
    
    def _parse_response(self, xml_text: str) -> Dict[str, Any]:
        """
        Parse SIFEN SOAP response.
        
        Returns:
            Dict with response_code, response_message, and other data
        """
        try:
            # Remove BOM if present
            if xml_text.startswith('\ufeff'):
                xml_text = xml_text[1:]
            
            root = etree.fromstring(xml_text.encode("UTF-8"))
            
            # Common response fields
            result = {
                "response_code": "UNKNOWN",
                "response_message": "Respuesta no procesada",
            }
            
            # Try to find response code (various possible locations)
            for xpath in [
                f".//{{{self.NS}}}dCodRes",
                ".//dCodRes",
                f".//{{{self.NS}}}gResProcDE/dCodRes",
            ]:
                elem = root.find(xpath)
                if elem is not None and elem.text:
                    result["response_code"] = elem.text
                    break
            
            # Try to find response message
            for xpath in [
                f".//{{{self.NS}}}dMsgRes",
                ".//dMsgRes",
                f".//{{{self.NS}}}gResProcDE/dMsgRes",
            ]:
                elem = root.find(xpath)
                if elem is not None and elem.text:
                    result["response_message"] = elem.text
                    break
            
            # Look for additional data
            # CDC in response
            cdc_elem = root.find(f".//{{{self.NS}}}dCDC")
            if cdc_elem is not None:
                result["cdc"] = cdc_elem.text
            
            # Processing ID
            id_elem = root.find(f".//{{{self.NS}}}dId")
            if id_elem is not None:
                result["processing_id"] = id_elem.text
            
            return result
            
        except Exception as e:
            return {
                "response_code": "PARSE_ERROR",
                "response_message": f"Error parsing response: {str(e)}",
            }
    
    def _make_request(
        self,
        endpoint: str,
        body: str,
        action: str,
    ) -> SifenResponse:
        """
        Make SOAP request to SIFEN.
        
        Args:
            endpoint: URL endpoint (relative to base_url)
            body: SOAP body content
            action: Action name for logging
        
        Returns:
            SifenResponse with result
        """
        start_time = time.time()
        url = f"{self.base_url}{endpoint}"
        soap_request = self._build_soap_request(body)
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    url,
                    content=soap_request,
                    headers={
                        "Content-Type": "application/soap+xml; charset=utf-8",
                        "SOAPAction": f'"{self.NS}/{action}"',
                    },
                )
                response.raise_for_status()
                
            duration_ms = int((time.time() - start_time) * 1000)
            
            parsed = self._parse_response(response.text)
            success = parsed["response_code"] in ["0", "0260"]  # 0260 = already exists
            
            # Log request
            SifenLog.objects.create(
                action=action,
                cdc=parsed.get("cdc", ""),
                request_xml=soap_request[:2000],
                response_xml=response.text[:2000],
                response_code=parsed["response_code"],
                response_message=parsed["response_message"][:500],
                duration_ms=duration_ms,
            )
            
            return SifenResponse(
                success=success,
                response_code=parsed["response_code"],
                response_message=parsed["response_message"],
                raw_xml=response.text,
                duration_ms=duration_ms,
                data=parsed,
            )
            
        except httpx.TimeoutException:
            duration_ms = int((time.time() - start_time) * 1000)
            return SifenResponse(
                success=False,
                response_code="TIMEOUT",
                response_message="Request timeout",
                raw_xml="",
                duration_ms=duration_ms,
            )
        except httpx.HTTPStatusError as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return SifenResponse(
                success=False,
                response_code=f"HTTP_{e.response.status_code}",
                response_message=str(e),
                raw_xml=e.response.text if hasattr(e.response, 'text') else "",
                duration_ms=duration_ms,
            )
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return SifenResponse(
                success=False,
                response_code="ERROR",
                response_message=str(e),
                raw_xml="",
                duration_ms=duration_ms,
            )
    
    def send_de(self, xml_de: str, id_lote: str = "1") -> SifenResponse:
        """
        Send electronic document to SIFEN (synchronous).
        
        Args:
            xml_de: Signed XML document
            id_lote: Batch ID (default "1" for single document)
        
        Returns:
            SifenResponse with result
        """
        body = f'''<rEnviDe xmlns="{self.NS}">
            <dId>{id_lote}</dId>
            <xDE>{xml_de}</xDE>
        </rEnviDe>'''
        
        return self._make_request("/de/ws/sync/recibe.wsdl", body, "send")
    
    def query_cdc(self, cdc: str) -> SifenResponse:
        """
        Query document status by CDC.
        
        Args:
            cdc: 44-character CDC code
        
        Returns:
            SifenResponse with document status
        """
        body = f'''<rConsDe xmlns="{self.NS}">
            <dCDC>{cdc}</dCDC>
        </rConsDe>'''
        
        return self._make_request("/de/ws/consulta/cdc.wsdl", body, "query")
    
    def query_ruc(self, ruc: str) -> SifenResponse:
        """
        Query taxpayer information by RUC.
        
        Args:
            ruc: RUC number (with or without check digit)
        
        Returns:
            SifenResponse with taxpayer data
        """
        # Extract RUC without check digit
        ruc_sin_dv = ruc.split("-")[0] if "-" in ruc else ruc
        
        body = f'''<rConsRUC xmlns="{self.NS}">
            <dRUCCons>{ruc_sin_dv}</dRUCCons>
        </rConsRUC>'''
        
        return self._make_request("/de/ws/consulta/ruc.wsdl", body, "query")
    
    def cancel_de(
        self,
        cdc: str,
        motivo: str = "Anulación solicitada",
    ) -> SifenResponse:
        """
        Cancel (annul) an electronic document.
        
        Args:
            cdc: CDC of document to cancel
            motivo: Cancellation reason
        
        Returns:
            SifenResponse with result
        """
        body = f'''<rEveAnuDE xmlns="{self.NS}">
            <dCDC>{cdc}</dCDC>
            <mOtEve>{motivo}</mOtEve>
        </rEveAnuDE>'''
        
        return self._make_request("/de/ws/evento/anulacion.wsdl", body, "cancel")
    
    def send_batch(self, documents: list, id_lote: str = None) -> SifenResponse:
        """
        Send multiple documents in a batch (async).
        
        Args:
            documents: List of signed XML documents
            id_lote: Batch ID (generated if not provided)
        
        Returns:
            SifenResponse with batch result
        """
        if not id_lote:
            id_lote = str(int(time.time()))
        
        # Build batch body
        xde_list = "".join(f"<xDE>{doc}</xDE>" for doc in documents)
        
        body = f'''<rEnviLoteDe xmlns="{self.NS}">
            <dId>{id_lote}</dId>
            {xde_list}
        </rEnviLoteDe>'''
        
        return self._make_request("/de/ws/async/recibe-lote.wsdl", body, "batch")


def get_soap_client() -> SifenSoapClient:
    """Get configured SOAP client."""
    return SifenSoapClient()
