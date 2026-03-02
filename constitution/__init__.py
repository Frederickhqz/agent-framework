"""
Constitutional Framework for Level 7 Self-Improving Agents

This module provides validation and enforcement of the constitutional principles
that govern agent self-improvement.
"""

from .validator import ConstitutionValidator, ValidationResult, RiskLevel

__version__ = "1.0.0"
__all__ = ["ConstitutionValidator", "ValidationResult", "RiskLevel"]