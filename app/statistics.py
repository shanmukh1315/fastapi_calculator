# app/statistics.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from app.db import get_db
from app.models import Calculation, User
from app.calculations import get_current_user

router = APIRouter()


@router.get("/statistics/summary")
def get_statistics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive usage statistics for the current user.
    
    Returns:
        - total_calculations: Total number of calculations performed
        - average_operand_a: Average value of operand 'a'
        - average_operand_b: Average value of operand 'b'
        - average_result: Average result value
        - most_used_operation: Most frequently used operation type
        - operations_breakdown: Count of each operation type
        - min_result: Minimum result value
        - max_result: Maximum result value
    """
    # Get all calculations for the user
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).all()
    
    if not calculations:
        return {
            "total_calculations": 0,
            "average_operand_a": 0,
            "average_operand_b": 0,
            "average_result": 0,
            "most_used_operation": None,
            "operations_breakdown": {},
            "min_result": None,
            "max_result": None
        }
    
    # Calculate aggregates
    total_calculations = len(calculations)
    
    # Average operands and results
    avg_a = sum(c.a for c in calculations) / total_calculations
    avg_b = sum(c.b for c in calculations) / total_calculations
    avg_result = sum(c.result for c in calculations) / total_calculations
    
    # Min/Max results
    min_result = min(c.result for c in calculations)
    max_result = max(c.result for c in calculations)
    
    # Operations breakdown
    operations_count = {}
    for calc in calculations:
        op_type = calc.type.value if hasattr(calc.type, 'value') else str(calc.type)
        operations_count[op_type] = operations_count.get(op_type, 0) + 1
    
    # Most used operation
    most_used_operation = max(operations_count.items(), key=lambda x: x[1])[0] if operations_count else None
    
    return {
        "total_calculations": total_calculations,
        "average_operand_a": round(avg_a, 2),
        "average_operand_b": round(avg_b, 2),
        "average_result": round(avg_result, 2),
        "most_used_operation": most_used_operation,
        "operations_breakdown": operations_count,
        "min_result": round(min_result, 2),
        "max_result": round(max_result, 2)
    }


@router.get("/statistics/recent")
def get_recent_statistics(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get statistics for the most recent N calculations.
    
    Args:
        limit: Number of recent calculations to analyze (default: 10)
        
    Returns:
        - count: Number of calculations analyzed
        - average_result: Average result of recent calculations
        - operations_used: List of operation types used
    """
    # Get recent calculations (ordered by ID descending)
    recent_calcs = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).order_by(Calculation.id.desc()).limit(limit).all()
    
    if not recent_calcs:
        return {
            "count": 0,
            "average_result": 0,
            "operations_used": []
        }
    
    avg_result = sum(c.result for c in recent_calcs) / len(recent_calcs)
    operations_used = [
        calc.type.value if hasattr(calc.type, 'value') else str(calc.type)
        for calc in recent_calcs
    ]
    
    return {
        "count": len(recent_calcs),
        "average_result": round(avg_result, 2),
        "operations_used": operations_used
    }
