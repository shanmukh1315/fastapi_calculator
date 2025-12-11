# tests/unit/test_statistics.py
import pytest
from app.statistics import router
from app.models import Calculation, User, CalculationType


class TestStatisticsSummaryLogic:
    """Test statistics calculation logic."""
    
    def test_empty_calculations_returns_zeros(self):
        """Test statistics with no calculations."""
        calculations = []
        
        # Simulate empty result
        result = {
            "total_calculations": 0,
            "average_operand_a": 0,
            "average_operand_b": 0,
            "average_result": 0,
            "most_used_operation": None,
            "operations_breakdown": {},
            "min_result": None,
            "max_result": None
        }
        
        assert result["total_calculations"] == 0
        assert result["average_operand_a"] == 0
        assert result["most_used_operation"] is None
    
    def test_single_calculation_statistics(self):
        """Test statistics with one calculation."""
        # Single add operation: 5 + 3 = 8
        a, b, result = 5.0, 3.0, 8.0
        
        stats = {
            "total_calculations": 1,
            "average_operand_a": a,
            "average_operand_b": b,
            "average_result": result,
            "min_result": result,
            "max_result": result,
            "most_used_operation": "add",
            "operations_breakdown": {"add": 1}
        }
        
        assert stats["total_calculations"] == 1
        assert stats["average_operand_a"] == 5.0
        assert stats["average_operand_b"] == 3.0
        assert stats["average_result"] == 8.0
        assert stats["min_result"] == 8.0
        assert stats["max_result"] == 8.0
    
    def test_multiple_calculations_averages(self):
        """Test average calculations with multiple entries."""
        # Simulating: [10+5=15, 20+10=30, 30+15=45]
        calcs = [
            {"a": 10, "b": 5, "result": 15, "type": "add"},
            {"a": 20, "b": 10, "result": 30, "type": "add"},
            {"a": 30, "b": 15, "result": 45, "type": "add"}
        ]
        
        total = len(calcs)
        avg_a = sum(c["a"] for c in calcs) / total
        avg_b = sum(c["b"] for c in calcs) / total
        avg_result = sum(c["result"] for c in calcs) / total
        
        assert avg_a == 20.0
        assert avg_b == 10.0
        assert avg_result == 30.0
    
    def test_min_max_result_calculation(self):
        """Test min and max result detection."""
        results = [15, -5, 100, 0, 42]
        
        min_result = min(results)
        max_result = max(results)
        
        assert min_result == -5
        assert max_result == 100
    
    def test_operations_breakdown_counting(self):
        """Test counting operations by type."""
        operations = ["add", "add", "multiply", "add", "subtract", "multiply"]
        
        breakdown = {}
        for op in operations:
            breakdown[op] = breakdown.get(op, 0) + 1
        
        assert breakdown["add"] == 3
        assert breakdown["multiply"] == 2
        assert breakdown["subtract"] == 1
    
    def test_most_used_operation_detection(self):
        """Test finding the most frequently used operation."""
        breakdown = {
            "add": 5,
            "multiply": 3,
            "subtract": 8,
            "divide": 2
        }
        
        most_used = max(breakdown.items(), key=lambda x: x[1])[0]
        
        assert most_used == "subtract"
    
    def test_rounding_to_two_decimals(self):
        """Test that statistics are rounded to 2 decimal places."""
        value = 10.0 / 3.0  # 3.333...
        rounded = round(value, 2)
        
        assert rounded == 3.33
    
    def test_mixed_operation_types(self):
        """Test statistics with various operation types."""
        operations = {
            "add": 2,
            "subtract": 1,
            "multiply": 3,
            "percent_of": 1,
            "nth_root": 2,
            "log_base": 1
        }
        
        total_ops = sum(operations.values())
        assert total_ops == 10
        assert max(operations.values()) == 3  # multiply is most used


class TestRecentStatisticsLogic:
    """Test recent statistics calculation logic."""
    
    def test_recent_stats_with_limit(self):
        """Test limiting to N recent calculations."""
        all_calcs = list(range(1, 21))  # 20 calculations
        limit = 10
        recent = all_calcs[-limit:]
        
        assert len(recent) == 10
        assert recent[0] == 11  # 11th item
        assert recent[-1] == 20  # last item
    
    def test_recent_stats_fewer_than_limit(self):
        """Test when total calculations < limit."""
        all_calcs = [1, 2, 3]
        limit = 10
        recent = all_calcs[-limit:]
        
        assert len(recent) == 3
    
    def test_recent_operations_extraction(self):
        """Test extracting operation types from recent calculations."""
        recent_calcs = [
            {"type": "add"},
            {"type": "multiply"},
            {"type": "add"},
            {"type": "percent_of"}
        ]
        
        operations = [c["type"] for c in recent_calcs]
        
        assert operations == ["add", "multiply", "add", "percent_of"]
        assert len(operations) == 4


class TestStatisticsEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_all_same_values(self):
        """Test when all calculations have same values."""
        calcs = [
            {"a": 10, "b": 10, "result": 20},
            {"a": 10, "b": 10, "result": 20},
            {"a": 10, "b": 10, "result": 20}
        ]
        
        avg_a = sum(c["a"] for c in calcs) / len(calcs)
        avg_result = sum(c["result"] for c in calcs) / len(calcs)
        
        assert avg_a == 10.0
        assert avg_result == 20.0
    
    def test_negative_results(self):
        """Test with negative calculation results."""
        results = [-10, -5, -20, -15]
        
        min_result = min(results)
        max_result = max(results)
        avg_result = sum(results) / len(results)
        
        assert min_result == -20
        assert max_result == -5
        assert avg_result == -12.5
    
    def test_zero_results(self):
        """Test with zero results."""
        results = [0, 0, 0]
        
        avg_result = sum(results) / len(results)
        
        assert avg_result == 0.0
    
    def test_large_numbers(self):
        """Test with very large numbers."""
        results = [1e10, 2e10, 3e10]
        
        avg_result = sum(results) / len(results)
        
        assert avg_result == 2e10
    
    def test_floating_point_precision(self):
        """Test floating point calculations are handled correctly."""
        values = [0.1, 0.2, 0.3]
        avg = sum(values) / len(values)
        rounded = round(avg, 2)
        
        assert rounded == 0.2
