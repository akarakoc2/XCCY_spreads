"""
Interactive OAS Spread Curve plotting with Plotly.
Allows hovering over points to see bond details.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from typing import Optional, Dict
from pathlib import Path

from ..engine.curve_fitting import NelsonSiegelSvensson, CurveFitter


class InteractiveOASPlotter:
    """
    Interactive plotter for OAS spread curves with hover information.
    """
    
    def __init__(self):
        """Initialize the interactive plotter."""
        self.nss = NelsonSiegelSvensson()
        self.fitter = CurveFitter()
    
    def plot_interactive_oas_curve(
        self,
        df: pd.DataFrame,
        duration_column: str = 'bid_years_to_wkout',
        oas_column: str = 'oas',
        bond_name_column: str = 'bond_name',
        title: str = "Interactive OAS Spread Curve",
        min_duration: float = 1.0,
        save_path: Optional[str] = None
    ) -> go.Figure:
        """
        Create an interactive OAS curve plot with hover information.
        
        Args:
            df: DataFrame containing bond data
            duration_column: Name of duration column
            oas_column: Name of OAS column
            bond_name_column: Name of bond name column
            title: Plot title
            min_duration: Minimum duration filter
            save_path: Optional path to save HTML file
            
        Returns:
            Plotly Figure object
        """
        # Clean and filter data
        df_clean = df.copy()
        df_clean[duration_column] = pd.to_numeric(df_clean[duration_column], errors='coerce')
        df_clean[oas_column] = pd.to_numeric(df_clean[oas_column], errors='coerce')
        
        # Filter
        df_clean = df_clean.dropna(subset=[duration_column, oas_column])
        df_clean = df_clean[df_clean[duration_column] >= min_duration]
        
        # Sort by duration
        df_clean = df_clean.sort_values(duration_column)
        
        print(f"Plotting {len(df_clean)} bonds")
        
        # Create figure
        fig = go.Figure()
        
        # Add scatter points with hover information
        hover_text = [
            f"<b>{row[bond_name_column]}</b><br>" +
            f"Duration: {row[duration_column]:.2f} years<br>" +
            f"OAS: {row[oas_column]:.2f} bps"
            for _, row in df_clean.iterrows()
        ]
        
        fig.add_trace(go.Scatter(
            x=df_clean[duration_column],
            y=df_clean[oas_column],
            mode='markers',
            name='Market Data',
            marker=dict(
                size=10,
                color='#1f77b4',
                line=dict(color='black', width=1)
            ),
            text=df_clean[bond_name_column],
            hovertext=hover_text,
            hoverinfo='text'
        ))
        
        # Fit NSS curve
        durations = df_clean[duration_column].values
        oas_values = df_clean[oas_column].values
        
        try:
            params, params_dict = self.nss.fit(durations, oas_values)
            
            # Generate smooth fitted curve
            x_smooth = np.linspace(durations.min(), durations.max(), 500)
            y_fit = self.nss.predict(x_smooth, params)
            
            fig.add_trace(go.Scatter(
                x=x_smooth,
                y=y_fit,
                mode='lines',
                name='NSS Fit',
                line=dict(color='#d62728', width=3),
                hoverinfo='skip'
            ))
            
            # Calculate fit metrics
            y_fit_actual = self.nss.predict(durations, params)
            fit_metrics = self.fitter.calculate_goodness_of_fit(oas_values, y_fit_actual)
            
            # Add annotation with fit statistics
            annotation_text = (
                f"<b>NSS Parameters:</b><br>"
                f"β₀: {params_dict['beta0_level']:.2f}<br>"
                f"β₁: {params_dict['beta1_slope']:.2f}<br>"
                f"β₂: {params_dict['beta2_curvature']:.2f}<br>"
                f"β₃: {params_dict['beta3_second_curvature']:.2f}<br>"
                f"<br><b>Fit Quality:</b><br>"
                f"R²: {fit_metrics['r_squared']:.4f}<br>"
                f"RMSE: {fit_metrics['rmse']:.2f} bps"
            )
            
            fig.add_annotation(
                text=annotation_text,
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                xanchor='left', yanchor='top',
                showarrow=False,
                bordercolor="black",
                borderwidth=1,
                bgcolor="rgba(255, 255, 255, 0.8)",
                font=dict(size=10)
            )
            
            print("\nNelson-Siegel-Svensson Fit Statistics:")
            print(f"  R²: {fit_metrics['r_squared']:.4f}")
            print(f"  RMSE: {fit_metrics['rmse']:.2f} bps")
            print(f"  MAE: {fit_metrics['mae']:.2f} bps")
            
        except Exception as e:
            print(f"NSS fitting failed: {e}")
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=18, family="Arial Black")
            ),
            xaxis_title="Duration (Years)",
            yaxis_title="OAS (bps)",
            hovermode='closest',
            template='plotly_white',
            width=1200,
            height=700,
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.02,
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="black",
                borderwidth=1
            )
        )
        
        # Save if requested
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(save_path)
            print(f"\nInteractive plot saved to {save_path}")
        
        return fig
    
    def show(self, fig: go.Figure):
        """Display the interactive figure in browser."""
        fig.show()
