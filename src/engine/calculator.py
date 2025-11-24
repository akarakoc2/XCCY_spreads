"""
Core calculation engine for XCCY spreads.
"""

from typing import List, Dict, Optional
from datetime import datetime
import numpy as np

from .models import CurrencyPair, SpreadData


class SpreadCalculator:
    """
    Engine for calculating cross-currency spreads.
    
    This class handles the core mathematical operations for computing
    spreads between currency pairs.
    """
    
    def __init__(self, risk_free_rates: Optional[Dict[str, float]] = None):
        """
        Initialize the spread calculator.
        
        Args:
            risk_free_rates: Dictionary of currency -> risk-free rate mappings
        """
        self.risk_free_rates = risk_free_rates or {}
    
    def calculate_spread(
        self, 
        currency_pair: CurrencyPair,
        forward_rate: float,
        spot_rate: float,
        time_period: float
    ) -> SpreadData:
        """
        Calculate the XCCY spread for a given currency pair.
        
        Args:
            currency_pair: The currency pair to calculate spread for
            forward_rate: Forward exchange rate
            spot_rate: Spot exchange rate
            time_period: Time period in years
            
        Returns:
            SpreadData object containing the calculated spread
        """
        # Calculate implied spread using covered interest parity
        spread = (forward_rate / spot_rate - 1) / time_period
        
        return SpreadData(
            currency_pair=currency_pair,
            spread=spread,
            timestamp=datetime.now()
        )
    
    def calculate_basis_spread(
        self,
        currency_pair: CurrencyPair,
        domestic_rate: float,
        foreign_rate: float,
        swap_rate: float
    ) -> SpreadData:
        """
        Calculate the basis spread using interest rate differential.
        
        Args:
            currency_pair: The currency pair
            domestic_rate: Domestic interest rate
            foreign_rate: Foreign interest rate
            swap_rate: Cross-currency swap rate
            
        Returns:
            SpreadData object with calculated basis spread
        """
        # Basis = Swap Rate - (Domestic Rate - Foreign Rate)
        spread = swap_rate - (domestic_rate - foreign_rate)
        
        return SpreadData(
            currency_pair=currency_pair,
            spread=spread,
            timestamp=datetime.now()
        )
    
    def calculate_time_series(
        self,
        currency_pair: CurrencyPair,
        rates_data: List[Dict[str, float]],
        calculation_method: str = "forward"
    ) -> List[SpreadData]:
        """
        Calculate spreads for a time series of rate data.
        
        Args:
            currency_pair: The currency pair
            rates_data: List of dictionaries containing rate information
            calculation_method: Method to use ("forward" or "basis")
            
        Returns:
            List of SpreadData objects
        """
        results = []
        
        for data_point in rates_data:
            if calculation_method == "forward":
                spread = self.calculate_spread(
                    currency_pair=currency_pair,
                    forward_rate=data_point.get('forward_rate', 0),
                    spot_rate=data_point.get('spot_rate', 1),
                    time_period=data_point.get('time_period', 1)
                )
            elif calculation_method == "basis":
                spread = self.calculate_basis_spread(
                    currency_pair=currency_pair,
                    domestic_rate=data_point.get('domestic_rate', 0),
                    foreign_rate=data_point.get('foreign_rate', 0),
                    swap_rate=data_point.get('swap_rate', 0)
                )
            else:
                raise ValueError(f"Unknown calculation method: {calculation_method}")
            
            results.append(spread)
        
        return results
    
    @staticmethod
    def interpolate_spread(
        known_spreads: List[float],
        known_tenors: List[float],
        target_tenor: float
    ) -> float:
        """
        Interpolate spread for a given tenor using linear interpolation.
        
        Args:
            known_spreads: List of known spread values
            known_tenors: List of known tenors (time periods)
            target_tenor: Target tenor to interpolate for
            
        Returns:
            Interpolated spread value
        """
        return float(np.interp(target_tenor, known_tenors, known_spreads))
