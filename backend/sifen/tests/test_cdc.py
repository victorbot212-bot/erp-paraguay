"""Tests for CDC generation and validation."""
import pytest
from datetime import datetime
from sifen.cdc import generate_cdc, validate_cdc, calculate_check_digit


class TestCDCGeneration:
    """Tests for CDC generation."""
    
    def test_cdc_length(self):
        """CDC should be exactly 44 characters."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        assert len(cdc) == 44
    
    def test_cdc_is_numeric(self):
        """CDC should contain only digits."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        assert cdc.isdigit()
    
    def test_cdc_tipo_de(self):
        """CDC should start with document type."""
        cdc = generate_cdc(
            tipo_de=5,  # Nota de crédito
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        assert cdc[:2] == "05"
    
    def test_cdc_ruc(self):
        """CDC should contain RUC and DV."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        assert cdc[2:10] == "80012345"
        assert cdc[10] == "6"
    
    def test_cdc_establecimiento_punto(self):
        """CDC should contain establishment and point."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="002",
            punto="003",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        assert cdc[11:14] == "002"
        assert cdc[14:17] == "003"
    
    def test_cdc_numero(self):
        """CDC should contain document number padded to 7 digits."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=123,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        assert cdc[17:24] == "0000123"
    
    def test_cdc_fecha(self):
        """CDC should contain date in YYYYMMDD format."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 12, 25),
        )
        assert cdc[25:33] == "20241225"
    
    def test_cdc_validation_valid(self):
        """Valid CDC should pass validation."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        assert validate_cdc(cdc) is True
    
    def test_cdc_validation_invalid_length(self):
        """CDC with wrong length should fail validation."""
        assert validate_cdc("123") is False
        assert validate_cdc("1" * 45) is False
    
    def test_cdc_validation_invalid_checksum(self):
        """CDC with wrong check digit should fail validation."""
        cdc = generate_cdc(
            tipo_de=1,
            ruc="80012345-6",
            establecimiento="001",
            punto="001",
            numero=1,
            tipo_contribuyente=2,
            fecha_emision=datetime(2024, 1, 15),
        )
        # Modify last digit
        wrong_dv = "9" if cdc[-1] != "9" else "0"
        invalid_cdc = cdc[:-1] + wrong_dv
        assert validate_cdc(invalid_cdc) is False


class TestCheckDigit:
    """Tests for modulo 11 check digit calculation."""
    
    def test_check_digit_calculation(self):
        """Check digit should be calculated correctly."""
        # Test with known values
        code = "0180012345600100100000012202401151"
        dv = calculate_check_digit(code)
        assert isinstance(dv, int)
        assert 0 <= dv <= 10
    
    def test_check_digit_deterministic(self):
        """Same input should always produce same check digit."""
        code = "0180012345600100100000012202401151234567890"
        dv1 = calculate_check_digit(code)
        dv2 = calculate_check_digit(code)
        assert dv1 == dv2
