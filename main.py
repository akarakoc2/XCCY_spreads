"""
XCCY Spreads - OAS Curve Analysis with Nelson-Siegel-Svensson Fitting

This script loads bond data and plots OAS spread curves using Bloomberg NIA-style
Nelson-Siegel-Svensson curve fitting.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Import modular components
from src.data import DataLoader
from src.visualization import OASCurvePlotter, InteractiveOASPlotter

# Load the dataset
print("Loading data from Data_WV_Sr.xlsx...")
loader = DataLoader()
df = loader.load_excel("Data_WV_Sr.xlsx")

# Clean up unnamed columns
df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
df.drop(columns=["Unnamed: 2"], inplace=True, errors='ignore')

print(f"Loaded {len(df)} bonds from dataset")
print(f"Columns: {list(df.columns)}")

# Extract durations and oas values
durations = df['bid_years_to_wkout'].values
oas_values = df['oas'].values

# Convert to numeric, forcing errors to NaN
durations = pd.to_numeric(durations, errors='coerce')
oas_values = pd.to_numeric(oas_values, errors='coerce')

# Remove NaN values and durations less than 1 year
valid_mask = ~(np.isnan(durations) | np.isnan(oas_values)) & (durations >= 1)
durations = durations[valid_mask]
oas_values = oas_values[valid_mask]

print(f"Valid data points (duration >= 1 year): {len(durations)}")

# Initialize OAS curve plotter
plotter = OASCurvePlotter()

# Plot OAS curve with Nelson-Siegel-Svensson fitting (no filters)
fig = plotter.plot_oas_curve_with_nss(
    durations=durations,
    oas_values=oas_values,
    title='OAS Spread Curve - Nelson-Siegel-Svensson Fit',
    filter_params={'max_oas': 10000, 'min_duration': 0},  # No filtering
    save_path='output/oas_curve_nss.png',
    show_stats=True
)

# Add overall title

plt.suptitle('OAS Spread Curve with Bloomberg NIA-Style Fitting', fontsize=12, y=0.98)

print("\n" + "="*60)
print("✓ Analysis completed!")
print("="*60)
print("\nCheck 'output/oas_curve_nss.png' for saved plot.")

# Create interactive plot with bond names
print("\n" + "="*60)
print("Creating interactive plot...")
print("="*60)

interactive_plotter = InteractiveOASPlotter()
fig_interactive = interactive_plotter.plot_interactive_oas_curve(
    df=df,
    duration_column='bid_years_to_wkout',
    oas_column='oas',
    bond_name_column='bond_name',
    title='Interactive OAS Spread Curve - Hover to See Bond Names',
    min_duration=1.0,
    save_path='output/oas_curve_interactive.html'
)

print("\n✓ Interactive plot saved to 'output/oas_curve_interactive.html'")
print("  Open this file in your browser to interact with the plot!")
print("\nDisplaying static plot window... (close window to exit)")

# Display the static plot
plotter.show()