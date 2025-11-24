"""
Advanced curve fitting models for spread analysis.
Includes Nelson-Siegel-Svensson and other curve fitting methodologies.
"""

import numpy as np
from typing import Tuple, Optional, Dict
from scipy.optimize import curve_fit
from scipy.interpolate import PchipInterpolator


class NelsonSiegelSvensson:
    """
    Nelson-Siegel-Svensson model for yield curve fitting.
    Used by Bloomberg for NIA curves.
    """
    
    @staticmethod
    def model(t: np.ndarray, beta0: float, beta1: float, beta2: float, 
              beta3: float, tau1: float, tau2: float) -> np.ndarray:
        """
        Nelson-Siegel-Svensson model function.
        
        Args:
            t: Time/duration array
            beta0: Level parameter
            beta1: Slope parameter
            beta2: Curvature parameter
            beta3: Second curvature parameter
            tau1: First decay parameter
            tau2: Second decay parameter
            
        Returns:
            Array of fitted values
        """
        term1 = beta0
        term2 = beta1 * ((1 - np.exp(-t/tau1)) / (t/tau1))
        term3 = beta2 * (((1 - np.exp(-t/tau1)) / (t/tau1)) - np.exp(-t/tau1))
        term4 = beta3 * (((1 - np.exp(-t/tau2)) / (t/tau2)) - np.exp(-t/tau2))
        return term1 + term2 + term3 + term4
    
    @staticmethod
    def fit(durations: np.ndarray, spreads: np.ndarray,
            initial_guess: Optional[list] = None) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Fit the Nelson-Siegel-Svensson model to spread data.
        
        Args:
            durations: Array of durations (x-axis)
            spreads: Array of spread values (y-axis)
            initial_guess: Optional initial parameter guesses
            
        Returns:
            Tuple of (fitted_parameters, parameters_dict)
        """
        if initial_guess is None:
            initial_guess = [
                np.mean(spreads),  # beta0 (level)
                -50,               # beta1 (slope)
                50,                # beta2 (curvature)
                0,                 # beta3 (second curvature)
                2.0,               # tau1
                5.0                # tau2
            ]
        
        params, _ = curve_fit(
            NelsonSiegelSvensson.model,
            durations,
            spreads,
            p0=initial_guess,
            maxfev=10000,
            bounds=(
                [-np.inf, -np.inf, -np.inf, -np.inf, 0.1, 0.1],  # Lower bounds
                [np.inf, np.inf, np.inf, np.inf, 20, 20]          # Upper bounds
            )
        )
        
        params_dict = {
            'beta0_level': params[0],
            'beta1_slope': params[1],
            'beta2_curvature': params[2],
            'beta3_second_curvature': params[3],
            'tau1': params[4],
            'tau2': params[5]
        }
        
        return params, params_dict
    
    @staticmethod
    def predict(durations: np.ndarray, params: np.ndarray) -> np.ndarray:
        """
        Predict spread values using fitted NSS parameters.
        
        Args:
            durations: Array of durations to predict for
            params: Fitted NSS parameters [beta0, beta1, beta2, beta3, tau1, tau2]
            
        Returns:
            Array of predicted spread values
        """
        return NelsonSiegelSvensson.model(durations, *params)


class CurveFitter:
    """
    General curve fitting class with multiple methods.
    """
    
    @staticmethod
    def fit_pchip(durations: np.ndarray, spreads: np.ndarray) -> PchipInterpolator:
        """
        Fit PCHIP (Piecewise Cubic Hermite Interpolating Polynomial).
        
        Args:
            durations: Array of durations
            spreads: Array of spread values
            
        Returns:
            Fitted PCHIP interpolator
        """
        return PchipInterpolator(durations, spreads)
    
    @staticmethod
    def calculate_goodness_of_fit(actual: np.ndarray, predicted: np.ndarray) -> Dict[str, float]:
        """
        Calculate goodness of fit metrics.
        
        Args:
            actual: Actual spread values
            predicted: Predicted spread values
            
        Returns:
            Dictionary with R-squared, RMSE, and MAE
        """
        # R-squared
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # RMSE
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        
        # MAE
        mae = np.mean(np.abs(actual - predicted))
        
        return {
            'r_squared': r_squared,
            'rmse': rmse,
            'mae': mae
        }
