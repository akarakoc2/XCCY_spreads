"""
Interactive dashboard for XCCY spreads visualization.
"""

import pandas as pd
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from .plotter import SpreadPlotter


class Dashboard:
    """
    Creates an interactive dashboard for visualizing spread data.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the dashboard with data.
        
        Args:
            data: DataFrame containing spread data
        """
        self.data = data
        self.plotter = SpreadPlotter()
        self.figures = []
    
    def create_overview_dashboard(
        self,
        date_column: str,
        spread_columns: List[str],
        save_path: Optional[str] = None
    ) -> None:
        """
        Create a comprehensive overview dashboard.
        
        Args:
            date_column: Name of the date column
            spread_columns: List of spread columns to visualize
            save_path: Optional path to save the dashboard
        """
        fig = plt.figure(figsize=(18, 10))
        
        # Time series plot
        ax1 = plt.subplot(2, 2, 1)
        for col in spread_columns:
            ax1.plot(self.data[date_column], self.data[col], label=col, linewidth=2)
        ax1.set_title('Spread Time Series', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Spread (bps)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Distribution plot
        ax2 = plt.subplot(2, 2, 2)
        for col in spread_columns:
            ax2.hist(self.data[col].dropna(), bins=30, alpha=0.5, label=col)
        ax2.set_title('Spread Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Spread (bps)')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Box plot
        ax3 = plt.subplot(2, 2, 3)
        self.data[spread_columns].boxplot(ax=ax3)
        ax3.set_title('Spread Box Plot', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Spread (bps)')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Summary statistics
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        
        stats_text = "Summary Statistics\n" + "="*40 + "\n\n"
        for col in spread_columns:
            stats = self.data[col].describe()
            stats_text += f"{col}:\n"
            stats_text += f"  Mean: {stats['mean']:.2f}\n"
            stats_text += f"  Std: {stats['std']:.2f}\n"
            stats_text += f"  Min: {stats['min']:.2f}\n"
            stats_text += f"  Max: {stats['max']:.2f}\n\n"
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace')
        
        plt.suptitle('XCCY Spreads Dashboard', fontsize=18, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dashboard saved to {save_path}")
        
        self.figures.append(fig)
    
    def create_comparison_dashboard(
        self,
        currency_pairs: List[str],
        metrics: Dict[str, pd.DataFrame],
        save_path: Optional[str] = None
    ) -> None:
        """
        Create a dashboard comparing multiple currency pairs.
        
        Args:
            currency_pairs: List of currency pair names
            metrics: Dictionary of metric_name -> DataFrame
            save_path: Optional path to save the dashboard
        """
        n_metrics = len(metrics)
        fig, axes = plt.subplots(n_metrics, 1, figsize=(16, 5*n_metrics))
        
        if n_metrics == 1:
            axes = [axes]
        
        for idx, (metric_name, df) in enumerate(metrics.items()):
            ax = axes[idx]
            
            for pair in currency_pairs:
                if pair in df.columns:
                    ax.plot(df.index, df[pair], label=pair, linewidth=2)
            
            ax.set_title(f'{metric_name}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Value')
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
        
        plt.suptitle('Currency Pair Comparison Dashboard', fontsize=18, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dashboard saved to {save_path}")
        
        self.figures.append(fig)
    
    def show_all(self) -> None:
        """Display all created dashboards."""
        plt.show()
    
    def close_all(self) -> None:
        """Close all dashboards."""
        for fig in self.figures:
            plt.close(fig)
        self.figures = []
