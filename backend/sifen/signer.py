"""
XML Digital Signature for SIFEN.
Uses XMLDSig Enveloped signature with PKCS#12 certificates.
"""
import os
from typing import Optional, Tuple
from lxml import etree

try:
    import xmlsec
    XMLSEC_AVAILABLE = True
except ImportError:
    XMLSEC_AVAILABLE = False

from django.conf import settings


class SifenSigner:
    """Signs XML documents for SIFEN using XMLDSig."""
    
    def __init__(
        self,
        cert_path: Optional[str] = None,
        cert_password: Optional[str] = None
    ):
        """
        Initialize signer with certificate.
        
        Args:
            cert_path: Path to PKCS#12 (.pfx/.p12) certificate
            cert_password: Certificate password
        """
        self.cert_path = cert_path or settings.SIFEN_CERT_PATH
        self.cert_password = cert_password or settings.SIFEN_CERT_PASSWORD
        self._key_manager = None
    
    @property
    def is_configured(self) -> bool:
        """Check if certificate is configured."""
        return bool(self.cert_path and os.path.exists(self.cert_path))
    
    def sign(self, xml_element: etree._Element) -> Tuple[etree._Element, str]:
        """
        Sign an XML document.
        
        Args:
            xml_element: lxml Element to sign (must have Id attribute on target)
        
        Returns:
            Tuple of (signed element, signature value)
        
        Raises:
            ValueError: If certificate not configured or signing fails
        """
        if not XMLSEC_AVAILABLE:
            raise ValueError("xmlsec library not available")
        
        if not self.is_configured:
            raise ValueError("Certificate not configured. Set SIFEN_CERT_PATH and SIFEN_CERT_PASSWORD")
        
        # Find the DE element with Id attribute
        de_element = xml_element.find(".//{http://ekuatia.set.gov.py/sifen/xsd}DE")
        if de_element is None:
            de_element = xml_element.find(".//DE")
        
        if de_element is None:
            raise ValueError("Cannot find DE element to sign")
        
        element_id = de_element.get("Id")
        if not element_id:
            raise ValueError("DE element must have Id attribute")
        
        # Create signature template
        signature_node = xmlsec.template.create(
            xml_element,
            c14n_method=xmlsec.constants.TransformExclC14N,
            sign_method=xmlsec.constants.TransformRsaSha256
        )
        
        # Add reference to the element with Id
        ref = xmlsec.template.add_reference(
            signature_node,
            digest_method=xmlsec.constants.TransformSha256,
            uri=f"#{element_id}"
        )
        
        # Add transforms
        xmlsec.template.add_transform(ref, xmlsec.constants.TransformEnveloped)
        xmlsec.template.add_transform(ref, xmlsec.constants.TransformExclC14N)
        
        # Add key info
        key_info = xmlsec.template.ensure_key_info(signature_node)
        xmlsec.template.add_x509_data(key_info)
        
        # Insert signature node into DE element
        de_element.append(signature_node)
        
        # Load key and sign
        ctx = xmlsec.SignatureContext()
        
        # Load PKCS#12 certificate
        key = xmlsec.Key.from_file(
            self.cert_path,
            format=xmlsec.constants.KeyDataFormatPkcs12,
            password=self.cert_password
        )
        ctx.key = key
        
        # Sign
        ctx.sign(signature_node)
        
        # Extract signature value
        sig_value = signature_node.find(".//{http://www.w3.org/2000/09/xmldsig#}SignatureValue")
        signature_value = sig_value.text if sig_value is not None else ""
        
        return xml_element, signature_value
    
    def sign_string(self, xml_string: str) -> str:
        """
        Sign an XML string.
        
        Args:
            xml_string: XML document as string
        
        Returns:
            Signed XML as string
        """
        xml_element = etree.fromstring(xml_string.encode("UTF-8"))
        signed_element, _ = self.sign(xml_element)
        return etree.tostring(
            signed_element,
            encoding="UTF-8",
            xml_declaration=True
        ).decode("UTF-8")


class MockSigner:
    """Mock signer for testing without real certificate."""
    
    def __init__(self):
        self.is_configured = True
    
    def sign(self, xml_element: etree._Element) -> Tuple[etree._Element, str]:
        """Add a mock signature for testing."""
        # Find DE element
        de_element = xml_element.find(".//{http://ekuatia.set.gov.py/sifen/xsd}DE")
        if de_element is None:
            de_element = xml_element.find(".//DE")
        
        if de_element is not None:
            # Add mock signature comment
            mock_sig = etree.Comment(" MOCK SIGNATURE - FOR TESTING ONLY ")
            de_element.append(mock_sig)
        
        return xml_element, "MOCK_SIGNATURE_VALUE"
    
    def sign_string(self, xml_string: str) -> str:
        xml_element = etree.fromstring(xml_string.encode("UTF-8"))
        signed_element, _ = self.sign(xml_element)
        return etree.tostring(
            signed_element,
            encoding="UTF-8",
            xml_declaration=True
        ).decode("UTF-8")


def get_signer(mock: bool = False) -> SifenSigner:
    """
    Get the appropriate signer.
    
    Args:
        mock: If True, return mock signer for testing
    
    Returns:
        SifenSigner or MockSigner instance
    """
    if mock or settings.SIFEN_ENVIRONMENT == "test":
        return MockSigner()
    return SifenSigner()
