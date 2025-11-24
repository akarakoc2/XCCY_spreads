"""
OAS Spread Curve plotting with Nelson-Siegel-Svensson fitting.
Specialized plotter for Option-Adjusted Spread analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Optional, Tuple, Dict
from pathlib import Path
import seaborn as sns

from ..engine.curve_fitting import NelsonSiegelSvensson, CurveFitter


class OASCurvePlotter:
    """
    Specialized plotter for OAS spread curves with Bloomberg NIA-style fitting.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize the OAS curve plotter.
        
        Args:
            style: Matplotlib style to use
        """
        self.style = style
        self.nss = NelsonSiegelSvensson()
        self.fitter = CurveFitter()
        
        try:
            plt.style.use(style)
        except:
            pass
    
    def plot_oas_curve_with_nss(
        self,
        durations: np.ndarray,
        oas_values: np.ndarray,
        title: str = "OAS Spread Curve - Nelson-Siegel-Svensson Fit",
        xlabel: str = "Duration (Years)",
        ylabel: str = "OAS (bps)",
        figsize: Tuple[int, int] = (12, 7),
        filter_params: Optional[Dict] = None,
        save_path: Optional[str] = None,
        show_stats: bool = True
    ) -> plt.Figure:
        """
        Plot OAS spread curve with Nelson-Siegel-Svensson fitting.
        
        Args:
            durations: Array of bond durations
            oas_values: Array of OAS spread values
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            filter_params: Dictionary with 'max_oas' and 'min_duration' filters
            save_path: Optional path to save the figure
            show_stats: Whether to display fitting statistics
            
        Returns:
            matplotlib Figure object
        """
        # Apply filters
        if filter_params is None:
            filter_params = {'max_oas': 150, 'min_duration': 1}
        
        valid = (
            (~np.isnan(durations)) & 
            (~np.isnan(oas_values)) & 
            (oas_values <= filter_params.get('max_oas', 150)) & 
            (durations >= filter_params.get('min_duration', 1))
        )
        
        durations_filtered = durations[valid]
        oas_filtered = oas_values[valid]
        
        print(f"Number of bonds after filtering (OAS <= {filter_params.get('max_oas', 150)} bps, "
              f"Duration >= {filter_params.get('min_duration', 1)} year): {len(oas_filtered)}")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Define colors
        color_scatter = '#1f77b4'  # Blue for scatter points
        color_fit = '#d62728'      # Red for fitted curve
        color_pchip = '#2ca02c'    # Green for PCHIP interpolation
        
        if len(durations_filtered) >= 2:
            # Sort data
            sort_idx = np.argsort(durations_filtered)
            durations_sorted = durations_filtered[sort_idx]
            oas_sorted = oas_filtered[sort_idx]
            
            # Scatter plot for actual data points
            ax.scatter(
                durations_sorted, oas_sorted, s=60, alpha=0.8,
                color=color_scatter, zorder=3, label='Market Data',
                edgecolors='black', linewidth=0.5
            )
            
            # Create smooth x-axis for curve fitting
            x_smooth = np.linspace(
                max(0.1, min(durations_sorted)),
                max(durations_sorted),
                500
            )
            
            # Try Nelson-Siegel-Svensson fitting
            try:
                params, params_dict = self.nss.fit(durations_sorted, oas_sorted)
                
                # Generate fitted curve
                y_fit = self.nss.predict(x_smooth, params)
                ax.plot(
                    x_smooth, y_fit, color=color_fit, linewidth=2.5,
                    label='Nelson-Siegel-Svensson Fit', zorder=2
                )
                
                # Calculate goodness of fit
                y_fit_actual = self.nss.predict(durations_sorted, params)
                fit_metrics = self.fitter.calculate_goodness_of_fit(
                    oas_sorted, y_fit_actual
                )
                
                # Print statistics
                if show_stats:
                    print("\nNelson-Siegel-Svensson parameters:")
                    print(f"  β₀ (Level): {params_dict['beta0_level']:.2f}")
                    print(f"  β₁ (Slope): {params_dict['beta1_slope']:.2f}")
                    print(f"  β₂ (Curvature): {params_dict['beta2_curvature']:.2f}")
                    print(f"  β₃ (Second Curvature): {params_dict['beta3_second_curvature']:.2f}")
                    print(f"  τ₁: {params_dict['tau1']:.2f}")
                    print(f"  τ₂: {params_dict['tau2']:.2f}")
                    print(f"\nGoodness of Fit:")
                    print(f"  R²: {fit_metrics['r_squared']:.4f}")
                    print(f"  RMSE: {fit_metrics['rmse']:.2f} bps")
                    print(f"  MAE: {fit_metrics['mae']:.2f} bps")
                
                # Add text box with fit statistics
                textstr = f"R² = {fit_metrics['r_squared']:.4f}\nRMSE = {fit_metrics['rmse']:.2f} bps"
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', bbox=props)
                
            except Exception as e:
                print(f"Nelson-Siegel-Svensson fitting failed: {e}")
                print("Falling back to PCHIP interpolation...")
                
                # Fallback to PCHIP interpolation
                if len(durations_sorted) >= 3:
                    try:
                        pchip = self.fitter.fit_pchip(durations_sorted, oas_sorted)
                        y_smooth = pchip(x_smooth)
                        ax.plot(
                            x_smooth, y_smooth, color=color_pchip, linewidth=2.5,
                            label='PCHIP Interpolation', zorder=2
                        )
                    except Exception as e2:
                        print(f"PCHIP interpolation also failed: {e2}")
                        ax.plot(
                            durations_sorted, oas_sorted, color=color_fit,
                            linewidth=2, label='Linear Connection', zorder=2
                        )
                else:
                    ax.plot(
                        durations_sorted, oas_sorted, color=color_fit,
                        linewidth=2, label='Linear Connection', zorder=2
                    )
        
        # Set titles and labels
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.set_xlim(0, None)
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        
        # Final layout adjustments
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nPlot saved to {save_path}")
        
        return fig
    
    def plot_oas_comparison(
        self,
        data_dict: Dict[str, Tuple[np.ndarray, np.ndarray]],
        title: str = "OAS Spread Curve Comparison",
        figsize: Tuple[int, int] = (14, 8),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Compare multiple OAS curves on the same plot.
        
        Args:
            data_dict: Dictionary mapping label -> (durations, oas_values)
            title: Plot title
            figsize: Figure size
            save_path: Optional path to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = sns.color_palette("husl", len(data_dict))
        
        for (label, (durations, oas_values)), color in zip(data_dict.items(), colors):
            # Filter and sort
            valid = (~np.isnan(durations)) & (~np.isnan(oas_values))
            dur_valid = durations[valid]
            oas_valid = oas_values[valid]
            
            sort_idx = np.argsort(dur_valid)
            dur_sorted = dur_valid[sort_idx]
            oas_sorted = oas_valid[sort_idx]
            
            # Plot scatter
            ax.scatter(dur_sorted, oas_sorted, alpha=0.6, color=color, 
                      s=40, label=f'{label} (Data)')
            
            # Fit NSS curve
            try:
                if len(dur_sorted) >= 6:
                    params, _ = self.nss.fit(dur_sorted, oas_sorted)
                    x_smooth = np.linspace(min(dur_sorted), max(dur_sorted), 200)
                    y_fit = self.nss.predict(x_smooth, params)
                    ax.plot(x_smooth, y_fit, color=color, linewidth=2,
                           label=f'{label} (NSS Fit)', linestyle='--')
            except Exception as e:
                print(f"Could not fit NSS for {label}: {e}")
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Duration (Years)', fontsize=12)
        ax.set_ylabel('OAS (bps)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        return fig
    
    @staticmethod
    def show():
        """Display all created plots."""
        plt.show()
    
    @staticmethod
    def close_all():
        """Close all plot windows."""
        plt.close('all')
