"""
Data models for XCCY spread calculations.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class CurrencyPair:
    """Represents a currency pair for XCCY spread calculation."""
    base_currency: str
    quote_currency: str
    
    def __str__(self) -> str:
        return f"{self.base_currency}/{self.quote_currency}"
    
    def __repr__(self) -> str:
        return f"CurrencyPair('{self.base_currency}', '{self.quote_currency}')"


@dataclass
class SpreadData:
    """Represents calculated spread data."""
    currency_pair: CurrencyPair
    spread: float
    timestamp: datetime
    basis_points: Optional[float] = None
    
    def __post_init__(self):
        """Calculate basis points if not provided."""
        if self.basis_points is None:
            self.basis_points = self.spread * 10000
    
    def __str__(self) -> str:
        return f"{self.currency_pair}: {self.spread:.4f} ({self.basis_points:.2f} bps)"
