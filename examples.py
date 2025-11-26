"""
Example usage of the XCCY Spreads toolkit.

This file demonstrates various ways to use the modular components
for spread analysis, data processing, and visualization.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Import toolkit components
from src.engine import CurrencyPair, NelsonSiegelSvensson
from src.data import DataLoader, DataProcessor, DataExporter
from src.visualization import SpreadPlotter, OASCurvePlotter, Dashboard



def example_2_oas_curve_fitting():
    """Example 2: OAS curve fitting with synthetic data"""
    print("\n" + "="*60)
    print("EXAMPLE 2: OAS Curve Fitting")
    print("="*60)
    
    # Generate synthetic OAS data
    np.random.seed(42)
    durations = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30])
    # OAS typically decreases then increases (U-shape curve)
    base_curve = 50 + 20 * np.exp(-durations/5) + 0.5 * durations
    noise = np.random.normal(0, 5, len(durations))
    oas_values = base_curve + noise
    
    # Plot with NSS fitting
    plotter = OASCurvePlotter()
    fig = plotter.plot_oas_curve_with_nss(
        durations=durations,
        oas_values=oas_values,
        title='Synthetic OAS Curve Example',
        filter_params={'max_oas': 200, 'min_duration': 0},
        save_path='output/example_oas_curve.png',
        show_stats=True
    )
    
    print("\n✓ OAS curve plot created and saved")


def example_3_time_series_analysis():
    """Example 3: Time series spread analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Time Series Spread Analysis")
    print("="*60)
    
    # Create synthetic time series data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    data = {
        'date': dates,
        'spread_usd_eur': 10 + 5 * np.sin(np.linspace(0, 4*np.pi, 100)) + np.random.normal(0, 1, 100),
        'spread_usd_gbp': 12 + 4 * np.cos(np.linspace(0, 4*np.pi, 100)) + np.random.normal(0, 1, 100)
    }
    df = pd.DataFrame(data)
    
    # Process data
    processor = DataProcessor()
    df['spread_usd_eur_ma7'] = processor.calculate_moving_average(df, 'spread_usd_eur', window=7)
    df['spread_usd_gbp_ma7'] = processor.calculate_moving_average(df, 'spread_usd_gbp', window=7)
    
    # Visualize
    plotter = SpreadPlotter()
    fig = plotter.plot_time_series(
        df=df,
        x_column='date',
        y_columns=['spread_usd_eur', 'spread_usd_eur_ma7'],
        title='USD/EUR Spread with 7-Day Moving Average',
        save_path='output/example_timeseries.png'
    )
    
    # Export data
    exporter = DataExporter()
    exporter.export_to_csv(df, 'output/example_spread_data.csv')
    
    print("\n✓ Time series analysis completed")
    print("✓ Data exported to CSV")


def example_4_multi_currency_comparison():
    """Example 4: Compare multiple currency pair spreads"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Multi-Currency Comparison")
    print("="*60)
    
    # Create synthetic data for multiple pairs
    dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
    data = {
        'date': dates,
        'USD_EUR': 10 + 2 * np.sin(np.linspace(0, 2*np.pi, 50)) + np.random.normal(0, 0.5, 50),
        'USD_GBP': 12 + 3 * np.sin(np.linspace(0, 2*np.pi, 50) + 1) + np.random.normal(0, 0.5, 50),
        'USD_JPY': 8 + 1.5 * np.sin(np.linspace(0, 2*np.pi, 50) + 2) + np.random.normal(0, 0.5, 50)
    }
    df = pd.DataFrame(data)
    
    # Create comparison plot
    plotter = SpreadPlotter()
    fig = plotter.plot_time_series(
        df=df,
        x_column='date',
        y_columns=['USD_EUR', 'USD_GBP', 'USD_JPY'],
        title='Cross-Currency Spread Comparison',
        ylabel='Spread (bps)',
        save_path='output/example_multi_currency.png'
    )
    
    print("\n✓ Multi-currency comparison plot created")


def example_5_dashboard():
    """Example 5: Create comprehensive dashboard"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Dashboard Creation")
    print("="*60)
    
    # Create synthetic data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    data = {
        'date': dates,
        'spread_usd_eur': 10 + 5 * np.sin(np.linspace(0, 4*np.pi, 100)) + np.random.normal(0, 1, 100),
        'spread_usd_gbp': 12 + 4 * np.cos(np.linspace(0, 4*np.pi, 100)) + np.random.normal(0, 1, 100)
    }
    df = pd.DataFrame(data)
    
    # Create dashboard
    dashboard = Dashboard(df)
    dashboard.create_overview_dashboard(
        date_column='date',
        spread_columns=['spread_usd_eur', 'spread_usd_gbp'],
        save_path='output/example_dashboard.png'
    )
    
    print("\n✓ Dashboard created and saved")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*60)
    print("XCCY SPREADS TOOLKIT - EXAMPLES")
    print("="*60)
    
    try:
        example_2_oas_curve_fitting()
        example_3_time_series_analysis()
        example_4_multi_currency_comparison()
        example_5_dashboard()
        
        print("\n" + "="*60)
        print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nCheck the 'output/' directory for generated files.")
        print("Close plot windows to exit.")
        
        # Show all plots
        import matplotlib.pyplot as plt
        plt.show()
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_examples()
