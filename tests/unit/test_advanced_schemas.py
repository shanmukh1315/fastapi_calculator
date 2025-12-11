# tests/unit/test_advanced_schemas.py
"""
Unit tests for Pydantic schema validation of advanced operations.
"""
import pytest
from pydantic import ValidationError

from app.schemas import CalculationBase, CalculationCreate
from app.models import CalculationType


class TestPercentOfSchemaValidation:
    """Test percent_of operation schema validation."""
    
    def test_percent_of_valid(self):
        """Valid percent_of calculation should pass."""
        calc = CalculationCreate(a=15, b=200, type=CalculationType.PERCENT_OF)
        assert calc.a == 15
        assert calc.b == 200
        assert calc.type == CalculationType.PERCENT_OF
    
    def test_percent_of_zero_percent(self):
        """0% of any number is valid."""
        calc = CalculationCreate(a=0, b=100, type=CalculationType.PERCENT_OF)
        assert calc.a == 0
    
    def test_percent_of_zero_base(self):
        """Any % of 0 is valid."""
        calc = CalculationCreate(a=50, b=0, type=CalculationType.PERCENT_OF)
        assert calc.b == 0
    
    def test_percent_of_negative_values(self):
        """Negative values should be allowed for percent_of."""
        calc = CalculationCreate(a=-10, b=50, type=CalculationType.PERCENT_OF)
        assert calc.a == -10


class TestNthRootSchemaValidation:
    """Test nth_root operation schema validation."""
    
    def test_nth_root_valid(self):
        """Valid nth_root calculation should pass."""
        calc = CalculationCreate(a=16, b=4, type=CalculationType.NTH_ROOT)
        assert calc.a == 16
        assert calc.b == 4
        assert calc.type == CalculationType.NTH_ROOT
    
    def test_nth_root_square_root(self):
        """Square root (b=2) is valid."""
        calc = CalculationCreate(a=25, b=2, type=CalculationType.NTH_ROOT)
        assert calc.b == 2
    
    def test_nth_root_cube_root(self):
        """Cube root (b=3) is valid."""
        calc = CalculationCreate(a=27, b=3, type=CalculationType.NTH_ROOT)
        assert calc.b == 3
    
    def test_nth_root_fractional_index(self):
        """Fractional root indices are valid at schema level."""
        calc = CalculationCreate(a=16, b=2.5, type=CalculationType.NTH_ROOT)
        assert calc.b == 2.5


class TestLogBaseSchemaValidation:
    """Test log_base operation schema validation."""
    
    def test_log_base_valid(self):
        """Valid log_base calculation should pass."""
        calc = CalculationCreate(a=8, b=2, type=CalculationType.LOG_BASE)
        assert calc.a == 8
        assert calc.b == 2
        assert calc.type == CalculationType.LOG_BASE
    
    def test_log_base_common_log(self):
        """Common logarithm (base 10) is valid."""
        calc = CalculationCreate(a=100, b=10, type=CalculationType.LOG_BASE)
        assert calc.b == 10
    
    def test_log_base_natural_log_approx(self):
        """Natural log approximation (base e) is valid."""
        calc = CalculationCreate(a=7.389, b=2.718, type=CalculationType.LOG_BASE)
        assert calc.b == 2.718


class TestAdvancedOperationsEnumCoverage:
    """Test that all advanced operations are in CalculationType enum."""
    
    def test_percent_of_in_enum(self):
        """PERCENT_OF should be in CalculationType."""
        assert hasattr(CalculationType, 'PERCENT_OF')
        assert CalculationType.PERCENT_OF.value == 'percent_of'
    
    def test_nth_root_in_enum(self):
        """NTH_ROOT should be in CalculationType."""
        assert hasattr(CalculationType, 'NTH_ROOT')
        assert CalculationType.NTH_ROOT.value == 'nth_root'
    
    def test_log_base_in_enum(self):
        """LOG_BASE should be in CalculationType."""
        assert hasattr(CalculationType, 'LOG_BASE')
        assert CalculationType.LOG_BASE.value == 'log_base'
    
    def test_all_nine_operations_present(self):
        """Should have exactly 9 calculation types."""
        expected = [
            'add', 'subtract', 'multiply', 'divide',
            'power', 'modulus',
            'percent_of', 'nth_root', 'log_base'
        ]
        actual = [member.value for member in CalculationType]
        assert len(actual) == 9
        for expected_type in expected:
            assert expected_type in actual


class TestSchemaStringRepresentation:
    """Test that advanced operations can be created from string values."""
    
    def test_percent_of_from_string(self):
        """Should accept 'percent_of' string for type."""
        calc = CalculationCreate(a=10, b=100, type='percent_of')
        assert calc.type == CalculationType.PERCENT_OF
    
    def test_nth_root_from_string(self):
        """Should accept 'nth_root' string for type."""
        calc = CalculationCreate(a=16, b=4, type='nth_root')
        assert calc.type == CalculationType.NTH_ROOT
    
    def test_log_base_from_string(self):
        """Should accept 'log_base' string for type."""
        calc = CalculationCreate(a=8, b=2, type='log_base')
        assert calc.type == CalculationType.LOG_BASE
    
    def test_invalid_type_string_raises_error(self):
        """Invalid operation type should raise ValidationError."""
        with pytest.raises(ValidationError):
            CalculationCreate(a=1, b=2, type='invalid_operation')


class TestCalculationBaseValidation:
    """Test CalculationBase schema with advanced operations."""
    
    def test_base_schema_accepts_new_types(self):
        """CalculationBase should accept new operation types."""
        for op_type in [CalculationType.PERCENT_OF, CalculationType.NTH_ROOT, CalculationType.LOG_BASE]:
            calc = CalculationBase(a=10, b=5, type=op_type)
            assert calc.type == op_type
    
    def test_division_by_zero_validator_ignores_new_ops(self):
        """Division by zero validator should not affect new operations."""
        # percent_of with b=0 is valid
        calc = CalculationBase(a=50, b=0, type=CalculationType.PERCENT_OF)
        assert calc.b == 0
        
        # nth_root with b=0 is schema-valid (backend will reject)
        calc = CalculationBase(a=16, b=0, type=CalculationType.NTH_ROOT)
        assert calc.b == 0
        
        # log_base with b=0 is schema-valid (backend will reject)
        calc = CalculationBase(a=8, b=0, type=CalculationType.LOG_BASE)
        assert calc.b == 0
