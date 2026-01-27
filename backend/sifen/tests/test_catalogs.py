"""Tests for SIFEN catalogs."""
import pytest
from sifen.catalogs import (
    DEPARTAMENTOS, get_departamento,
    ACTIVIDADES_ECONOMICAS, get_actividad, buscar_actividad,
    TIPOS_DOCUMENTO, get_tipo_documento,
    MONEDAS, get_moneda,
    TASAS_IVA, get_tasa_iva,
    UNIDADES_MEDIDA, get_unidad_medida,
)
from sifen.catalogs.departamentos import buscar_departamento, get_distrito
from sifen.catalogs.impuestos import calcular_iva, calcular_iva_desde_base
from sifen.catalogs.unidades import get_codigo_sifen


class TestDepartamentos:
    """Tests for departments catalog."""
    
    def test_all_departments_present(self):
        """All 18 departments should be present."""
        # 0-17 = 18 departments
        assert len(DEPARTAMENTOS) == 18
    
    def test_get_departamento(self):
        """get_departamento should return correct data."""
        central = get_departamento("11")
        assert central["nombre"] == "CENTRAL"
        assert "distritos" in central
    
    def test_get_departamento_invalid(self):
        """get_departamento with invalid code should return default."""
        result = get_departamento("99")
        assert result["nombre"] == "DESCONOCIDO"
    
    def test_get_distrito(self):
        """get_distrito should return district name."""
        # Asunción is district 1 of department 0
        distrito = get_distrito("0", "1")
        assert distrito == "ASUNCION"
    
    def test_buscar_departamento(self):
        """buscar_departamento should find by name."""
        codigo = buscar_departamento("central")
        assert codigo == "11"
    
    def test_central_has_districts(self):
        """Central department should have San Lorenzo."""
        central = get_departamento("11")
        distritos = central["distritos"]
        assert "14" in distritos
        assert distritos["14"] == "SAN LORENZO"


class TestActividades:
    """Tests for economic activities catalog."""
    
    def test_has_activities(self):
        """Catalog should have activities."""
        assert len(ACTIVIDADES_ECONOMICAS) > 50
    
    def test_get_actividad(self):
        """get_actividad should return description."""
        desc = get_actividad("47111")
        assert "Venta al por menor" in desc
    
    def test_get_actividad_invalid(self):
        """get_actividad with invalid code should return default."""
        desc = get_actividad("00000")
        assert desc == "Actividad no especificada"
    
    def test_buscar_actividad(self):
        """buscar_actividad should find matches."""
        results = buscar_actividad("farmac")
        assert len(results) > 0
        assert any("farmac" in r["descripcion"].lower() for r in results)
    
    def test_buscar_actividad_short_term(self):
        """buscar_actividad with single char should return empty (min is 2)."""
        results = buscar_actividad("q")  # Single char, function requires min 2
        assert len(results) == 0  # min length is 2


class TestDocumentos:
    """Tests for document types catalog."""
    
    def test_tipos_documento(self):
        """Should have identity document types."""
        assert "1" in TIPOS_DOCUMENTO  # CI
        assert "2" in TIPOS_DOCUMENTO  # Pasaporte
    
    def test_get_tipo_documento(self):
        """get_tipo_documento should return description."""
        desc = get_tipo_documento("1")
        assert "Cédula" in desc


class TestMonedas:
    """Tests for currencies catalog."""
    
    def test_has_pyg(self):
        """Catalog should have Guarani."""
        assert "PYG" in MONEDAS
        assert MONEDAS["PYG"]["decimales"] == 0
    
    def test_has_usd(self):
        """Catalog should have US Dollar."""
        assert "USD" in MONEDAS
        assert MONEDAS["USD"]["decimales"] == 2
    
    def test_get_moneda(self):
        """get_moneda should return currency info."""
        pyg = get_moneda("PYG")
        assert pyg["nombre"] == "Guaraní"
        assert pyg["simbolo"] == "₲"


class TestImpuestos:
    """Tests for tax catalog."""
    
    def test_tasas_iva(self):
        """Should have all IVA rates."""
        assert 10 in TASAS_IVA
        assert 5 in TASAS_IVA
        assert 0 in TASAS_IVA
    
    def test_get_tasa_iva(self):
        """get_tasa_iva should return rate info."""
        tasa = get_tasa_iva(10)
        assert tasa["descripcion"] == "IVA 10%"
    
    def test_calcular_iva_10(self):
        """calcular_iva should calculate 10% correctly."""
        # 1,000,000 con IVA incluido
        result = calcular_iva(1000000, 10)
        assert result["iva"] == pytest.approx(90909.09, rel=0.01)
        assert result["total"] == 1000000
    
    def test_calcular_iva_5(self):
        """calcular_iva should calculate 5% correctly."""
        result = calcular_iva(1050000, 5)
        assert result["iva"] == pytest.approx(50000, rel=0.01)
    
    def test_calcular_iva_exento(self):
        """calcular_iva should handle exempt correctly."""
        result = calcular_iva(1000000, 0)
        assert result["iva"] == 0
        assert result["base_sin_iva"] == 1000000
    
    def test_calcular_iva_desde_base(self):
        """calcular_iva_desde_base should add IVA correctly."""
        result = calcular_iva_desde_base(909091, 10)
        assert result["iva"] == pytest.approx(90909.1, rel=0.01)
        assert result["total"] == pytest.approx(1000000.1, rel=0.01)


class TestUnidades:
    """Tests for units of measure catalog."""
    
    def test_has_unidad(self):
        """Catalog should have unit."""
        assert "77" in UNIDADES_MEDIDA
        assert UNIDADES_MEDIDA["77"]["codigo"] == "UNI"
    
    def test_get_unidad_medida(self):
        """get_unidad_medida should return unit info."""
        unidad = get_unidad_medida("83")
        assert unidad["codigo"] == "KG"
    
    def test_get_codigo_sifen(self):
        """get_codigo_sifen should return SIFEN code."""
        codigo = get_codigo_sifen("KG")
        assert codigo == "83"
    
    def test_get_codigo_sifen_default(self):
        """get_codigo_sifen should return default for unknown."""
        codigo = get_codigo_sifen("UNKNOWN")
        assert codigo == "77"  # Default: Unidad
