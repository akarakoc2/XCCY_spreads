"""
Plotting utilities for visualizing XCCY spreads.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Optional, Tuple, Dict
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


class SpreadPlotter:
    """
    Handles creating various plots and visualizations for spread data.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize the plotter with a matplotlib style.
        
        Args:
            style: Matplotlib style to use
        """
        self.style = style
        try:
            plt.style.use(style)
        except:
            pass  # Use default if style not available
    
    def plot_time_series(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        title: str = "XCCY Spread Time Series",
        xlabel: str = "Date",
        ylabel: str = "Spread (bps)",
        figsize: Tuple[int, int] = (14, 7),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot time series data for spreads.
        
        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis (typically date)
            y_columns: List of column names to plot
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            save_path: Optional path to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for col in y_columns:
            ax.plot(df[x_column], df[col], label=col, linewidth=2)
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        return fig
    
    def plot_spread_comparison(
        self,
        df: pd.DataFrame,
        category_column: str,
        value_column: str,
        title: str = "Spread Comparison",
        figsize: Tuple[int, int] = (12, 6),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create a bar plot comparing spreads across categories.
        
        Args:
            df: DataFrame containing the data
            category_column: Column for categories (x-axis)
            value_column: Column for values (y-axis)
            title: Plot title
            figsize: Figure size
            save_path: Optional path to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        df_sorted = df.sort_values(by=value_column, ascending=False)
        
        bars = ax.bar(
            df_sorted[category_column],
            df_sorted[value_column],
            color=sns.color_palette("husl", len(df_sorted))
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(category_column, fontsize=12)
        ax.set_ylabel(value_column, fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.2f}',
                ha='center',
                va='bottom',
                fontsize=9
            )
        
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        return fig
    
    def plot_heatmap(
        self,
        df: pd.DataFrame,
        title: str = "Spread Correlation Heatmap",
        figsize: Tuple[int, int] = (10, 8),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create a correlation heatmap.
        
        Args:
            df: DataFrame containing numeric data
            title: Plot title
            figsize: Figure size
            save_path: Optional path to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate correlation matrix
        corr = df.select_dtypes(include=['float64', 'int64']).corr()
        
        # Create heatmap
        sns.heatmap(
            corr,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        return fig
    
    def plot_distribution(
        self,
        df: pd.DataFrame,
        column: str,
        title: str = "Spread Distribution",
        bins: int = 30,
        figsize: Tuple[int, int] = (12, 6),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot distribution of spread values.
        
        Args:
            df: DataFrame containing the data
            column: Column name to plot distribution for
            title: Plot title
            bins: Number of bins for histogram
            figsize: Figure size
            save_path: Optional path to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Histogram
        ax.hist(df[column], bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Add mean and median lines
        mean_val = df[column].mean()
        median_val = df[column].median()
        
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        return fig
    
    def plot_multi_panel(
        self,
        df: pd.DataFrame,
        plots_config: List[Dict],
        title: str = "XCCY Spreads Dashboard",
        figsize: Tuple[int, int] = (16, 12),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create a multi-panel figure with different plots.
        
        Args:
            df: DataFrame containing the data
            plots_config: List of dictionaries specifying plot configurations
            title: Overall figure title
            figsize: Figure size
            save_path: Optional path to save the figure
            
        Returns:
            matplotlib Figure object
        """
        n_plots = len(plots_config)
        n_cols = 2
        n_rows = (n_plots + 1) // 2
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        fig.suptitle(title, fontsize=18, fontweight='bold')
        
        if n_plots == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for idx, config in enumerate(plots_config):
            ax = axes[idx]
            plot_type = config.get('type', 'line')
            
            if plot_type == 'line':
                for col in config['y_columns']:
                    ax.plot(df[config['x_column']], df[col], label=col)
                ax.legend()
            elif plot_type == 'bar':
                ax.bar(df[config['x_column']], df[config['y_column']])
            
            ax.set_title(config.get('title', ''), fontsize=12)
            ax.set_xlabel(config.get('xlabel', ''))
            ax.set_ylabel(config.get('ylabel', ''))
            ax.grid(True, alpha=0.3)
        
        # Hide unused subplots
        for idx in range(n_plots, len(axes)):
            axes[idx].set_visible(False)
        
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
