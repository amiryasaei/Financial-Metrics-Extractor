"""
Metrics utilities for parsing and managing financial metrics.
"""

from typing import List, Dict


def parse_custom_metrics(custom_input: str) -> List[str]:
    """
    Parse comma-separated custom metrics.
    
    Args:
        custom_input: Comma-separated string of metric names
        
    Returns:
        list: List of cleaned metric names
    """
    if not custom_input:
        return []
    
    metrics = [m.strip().replace(' ', '_') for m in custom_input.split(',')]
    return [m for m in metrics if m]


def get_available_metrics() -> Dict[str, str]:
    """
    Get dictionary of available predefined metrics.
    
    Returns:
        dict: Mapping of metric keys to display names
    """
    return {
        'revenue': 'Revenue',
        'gross_margin': 'Gross Margin',
        'headcount': 'Headcount',
        'arr': 'ARR (Annual Recurring Revenue)'
    }

