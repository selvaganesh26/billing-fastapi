from typing import Dict, List
from app.core.exceptions import InsufficientDenominationException


def calculate_change_denominations(
    change_amount: float,
    available_denominations: Dict[int, int]
) -> Dict[int, int]:
    """
    Calculate optimal denomination breakdown for change.
    Uses greedy algorithm (largest first).
    
    Args:
        change_amount: Amount of change to give
        available_denominations: Dict of {denomination_value: available_count}
    
    Returns:
        Dict of {denomination_value: count_to_give}
    
    Raises:
        InsufficientDenominationException: If change cannot be given
    """
    if change_amount == 0:
        return {}
    
    change_amount = int(change_amount)
    result = {}
    
    # Sort denominations in descending order
    sorted_denoms = sorted(available_denominations.keys(), reverse=True)
    
    for denom in sorted_denoms:
        if change_amount == 0:
            break
            
        available = available_denominations[denom]
        needed = change_amount // denom
        
        if needed > 0:
            count_to_give = min(needed, available)
            if count_to_give > 0:
                result[denom] = count_to_give
                change_amount -= denom * count_to_give
    
    if change_amount > 0:
        raise InsufficientDenominationException(
            f"Cannot provide exact change. Remaining: {change_amount}",
            details={"remaining": change_amount}
        )
    
    return result
