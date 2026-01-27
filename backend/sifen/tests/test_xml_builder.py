"""Tests for XML builder."""
import pytest
from datetime import datetime
from lxml import etree
from sifen.xml_builder import SifenXMLBuilder


class TestXMLBuilder:
    """Tests for SIFEN XML builder."""
    
    @pytest.fixture
    def builder(self):
        return SifenXMLBuilder()
    
    @pytest.fixture
    def sample_invoice_data(self):
        return {
            "cdc": "01800123456001001000000012202401151234567890",
            "tipo_de": 1,
            "fecha_emision": datetime(2024, 1, 15, 10, 30, 0),
            "emisor_ruc": "80012345-6",
            "emisor_razon_social": "Empresa Test S.A.",
            "emisor_nombre_fantasia": "Test Corp",
            "emisor_actividad": "47111",
            "emisor_timbrado": "12345678",
            "emisor_establecimiento": "001",
            "emisor_punto": "001",
            "emisor_numero": 1,
            "emisor_direccion": "Av. España 1234",
            "emisor_departamento": "Central",
            "emisor_distrito": "Asunción",
            "emisor_ciudad": "Asunción",
            "receptor_contribuyente": True,
            "receptor_ruc": "12345678-9",
            "receptor_razon_social": "Cliente Test",
            "total": 1000000,
            "total_iva_10": 1000000,
            "items": [{
                "codigo": "PROD001",
                "descripcion": "Producto de prueba",
                "cantidad": 1,
                "precio_unitario": 1000000,
                "unidad_medida": "Unidad",
                "tasa_iva": 10,
                "subtotal": 1000000,
                "iva": 90909,
                "total": 1000000,
            }]
        }
    
    def test_build_de_returns_element(self, builder, sample_invoice_data):
        """build_de should return an lxml Element."""
        result = builder.build_de(**sample_invoice_data)
        assert isinstance(result, etree._Element)
    
    def test_root_element_is_rde(self, builder, sample_invoice_data):
        """Root element should be rDE."""
        result = builder.build_de(**sample_invoice_data)
        # Check local name without namespace
        assert result.tag.endswith("rDE") or result.tag == "rDE"
    
    def test_has_version(self, builder, sample_invoice_data):
        """XML should have version element."""
        result = builder.build_de(**sample_invoice_data)
        version = result.find(".//{http://ekuatia.set.gov.py/sifen/xsd}dVerFor")
        if version is None:
            version = result.find(".//dVerFor")
        assert version is not None
        assert version.text == "150"
    
    def test_has_de_with_id(self, builder, sample_invoice_data):
        """XML should have DE element with Id attribute."""
        result = builder.build_de(**sample_invoice_data)
        de = result.find(".//{http://ekuatia.set.gov.py/sifen/xsd}DE")
        if de is None:
            de = result.find(".//DE")
        assert de is not None
        assert de.get("Id") == sample_invoice_data["cdc"]
    
    def test_has_emisor_data(self, builder, sample_invoice_data):
        """XML should have emisor data."""
        result = builder.build_de(**sample_invoice_data)
        xml_str = builder.to_string()
        
        assert "80012345" in xml_str  # RUC
        assert "Empresa Test S.A." in xml_str
    
    def test_has_receptor_data(self, builder, sample_invoice_data):
        """XML should have receptor data."""
        result = builder.build_de(**sample_invoice_data)
        xml_str = builder.to_string()
        
        assert "12345678" in xml_str  # Receptor RUC
        assert "Cliente Test" in xml_str
    
    def test_has_items(self, builder, sample_invoice_data):
        """XML should have item data."""
        result = builder.build_de(**sample_invoice_data)
        xml_str = builder.to_string()
        
        assert "Producto de prueba" in xml_str
        assert "1000000" in xml_str
    
    def test_to_string_returns_utf8(self, builder, sample_invoice_data):
        """to_string should return UTF-8 encoded string."""
        builder.build_de(**sample_invoice_data)
        result = builder.to_string()
        
        assert isinstance(result, str)
        assert "<?xml version" in result
        assert "UTF-8" in result
    
    def test_to_string_pretty_print(self, builder, sample_invoice_data):
        """to_string with pretty=True should include newlines."""
        builder.build_de(**sample_invoice_data)
        
        result_pretty = builder.to_string(pretty=True)
        result_compact = builder.to_string(pretty=False)
        
        assert result_pretty.count("\n") > result_compact.count("\n")
    
    def test_multiple_items(self, builder, sample_invoice_data):
        """XML should handle multiple items."""
        sample_invoice_data["items"] = [
            {
                "codigo": "PROD001",
                "descripcion": "Producto 1",
                "cantidad": 1,
                "precio_unitario": 500000,
                "unidad_medida": "Unidad",
                "tasa_iva": 10,
                "subtotal": 500000,
                "iva": 45454,
                "total": 500000,
            },
            {
                "codigo": "PROD002",
                "descripcion": "Producto 2",
                "cantidad": 2,
                "precio_unitario": 250000,
                "unidad_medida": "Unidad",
                "tasa_iva": 10,
                "subtotal": 500000,
                "iva": 45455,
                "total": 500000,
            },
        ]
        
        result = builder.build_de(**sample_invoice_data)
        xml_str = builder.to_string()
        
        assert "Producto 1" in xml_str
        assert "Producto 2" in xml_str
    
    def test_non_contributor_receptor(self, builder, sample_invoice_data):
        """XML should handle non-contributor receptor."""
        sample_invoice_data["receptor_contribuyente"] = False
        sample_invoice_data["receptor_ruc"] = ""
        sample_invoice_data["receptor_tipo_doc"] = 1
        sample_invoice_data["receptor_num_doc"] = "1234567"
        
        result = builder.build_de(**sample_invoice_data)
        xml_str = builder.to_string()
        
        # Should have B2C operation type
        assert "iTiOpe" in xml_str
