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
from src.visualization import OASCurvePlotter

# Load the dataset
print("Loading data from Data.xlsx...")
loader = DataLoader()
df = loader.load_excel("Data.xlsx")

# Clean up unnamed columns
df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
df.drop(columns=["Unnamed: 2"], inplace=True, errors='ignore')

print(f"Loaded {len(df)} bonds from dataset")
print(f"Columns: {list(df.columns)}")

# Extract durations and oas values
durations = df['bid_years_to_wkout'].values
oas_values = df['oas'].values

# Initialize OAS curve plotter
plotter = OASCurvePlotter()

# Plot OAS curve with Nelson-Siegel-Svensson fitting
fig = plotter.plot_oas_curve_with_nss(
    durations=durations,
    oas_values=oas_values,
    title='OAS Spread Curve - Nelson-Siegel-Svensson Fit',
    filter_params={'max_oas': 120, 'min_duration': 1},
    save_path='output/oas_curve_nss.png',
    show_stats=True
)

# Add overall title

plt.suptitle('OAS Spread Curve with Bloomberg NIA-Style Fitting', fontsize=12, y=0.98)

print("\n" + "="*60)
print("✓ Analysis completed!")
print("="*60)

# Display the plot
plotter.show()