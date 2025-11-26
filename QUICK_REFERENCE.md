# XCCY Spreads - Quick Reference Guide

## 🚀 Quick Start

### Run the main OAS analysis:
```bash
python main.py
```

### Run example demonstrations:
```bash
python examples.py
```

## 📦 Module Import Guide

### Engine Module - Calculations
```python
# Curve fitting
from src.engine import NelsonSiegelSvensson, CurveFitter

nss = NelsonSiegelSvensson()
params, params_dict = nss.fit(durations, spreads)
fitted_values = nss.predict(durations, params)
```

### Data Module - Data Handling
```python
# Loading data
from src.data import DataLoader

loader = DataLoader()
df = loader.load_excel("Data.xlsx")
df_csv = loader.load_csv("data.csv", date_column="date")

# Processing data
from src.data import DataProcessor

processor = DataProcessor()
df_clean = processor.clean_data(df, drop_na=True)
df['ma'] = processor.calculate_moving_average(df, 'spread', window=7)
df_resampled = processor.resample_timeseries(df, 'date', frequency='W')

# Exporting data
from src.data import DataExporter

exporter = DataExporter()
exporter.export_to_csv(df, 'output/results.csv')
exporter.export_to_excel(df, 'output/results.xlsx', sheet_name='Spreads')
```

### Visualization Module - Plotting
```python
# General plotting
from src.visualization import SpreadPlotter

plotter = SpreadPlotter()
plotter.plot_time_series(df, x_column='date', y_columns=['spread1', 'spread2'])
plotter.plot_distribution(df, column='spread', bins=30)
plotter.plot_heatmap(df, title='Correlation Matrix')
plotter.show()

# OAS-specific plotting
from src.visualization import OASCurvePlotter

oas_plotter = OASCurvePlotter()
fig = oas_plotter.plot_oas_curve_with_nss(
    durations=durations,
    oas_values=oas,
    filter_params={'max_oas': 150, 'min_duration': 1},
    save_path='output/oas_curve.png'
)

# Dashboard
from src.visualization import Dashboard

dashboard = Dashboard(df)
dashboard.create_overview_dashboard(
    date_column='date',
    spread_columns=['spread1', 'spread2']
)
```

## 🔧 Configuration

Edit `config/config.json` to customize:
```python
from config import get_config

config = get_config()
max_oas = config.get('oas_analysis.max_oas_filter')
fig_size = config.get('visualization.figure_size')
```

## 📊 Common Workflows

### 1. OAS Curve Analysis
```python
from src.data import DataLoader
from src.visualization import OASCurvePlotter

loader = DataLoader()
df = loader.load_excel("bonds.xlsx")

plotter = OASCurvePlotter()
plotter.plot_oas_curve_with_nss(
    durations=df['duration'].values,
    oas_values=df['oas'].values,
    save_path='output/oas_curve.png'
)
plotter.show()
```

### 2. Time Series Spread Analysis
```python
from src.data import DataLoader, DataProcessor
from src.visualization import SpreadPlotter

# Load and process
loader = DataLoader()
df = loader.load_csv("spreads.csv", date_column='date')

processor = DataProcessor()
df['ma7'] = processor.calculate_moving_average(df, 'spread', 7)
df['ma30'] = processor.calculate_moving_average(df, 'spread', 30)

# Visualize
plotter = SpreadPlotter()
plotter.plot_time_series(
    df, x_column='date',
    y_columns=['spread', 'ma7', 'ma30'],
    save_path='output/spread_analysis.png'
)
plotter.show()
```

## 📝 Data Format Requirements

### For OAS Analysis
Excel/CSV file should contain:
- `bid_years_to_wkout` or `duration`: Bond duration in years
- `oas`: Option-Adjusted Spread in basis points

### For Time Series Analysis
CSV/Excel should contain:
- Date column (specify name)
- One or more numeric spread columns

## 🎨 Customization

### Custom Plot Colors
```python
plotter = SpreadPlotter()
fig, ax = plotter.plot_time_series(...)
ax.lines[0].set_color('#FF5733')  # Change line color
```

### Custom Filter Parameters
```python
filter_params = {
    'max_oas': 200,      # Maximum OAS in bps
    'min_duration': 0.5, # Minimum duration in years
}
plotter.plot_oas_curve_with_nss(..., filter_params=filter_params)
```

## 🐛 Troubleshooting

### Import Errors
Make sure you're in the project root directory and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Data Loading Issues
Check column names match expected format:
```python
loader = DataLoader()
df = loader.load_excel("file.xlsx")
print(df.columns)  # Verify column names
```

### NSS Fitting Fails
If NSS fitting fails, the system automatically falls back to PCHIP interpolation. To force NSS:
```python
from src.engine import NelsonSiegelSvensson

nss = NelsonSiegelSvensson()
try:
    params, params_dict = nss.fit(durations, spreads)
except Exception as e:
    print(f"Fitting failed: {e}")
```

## 📚 Additional Resources

- **README.md**: Full documentation
- **examples.py**: Comprehensive usage examples
- **config/config.json**: Configuration options
- **src/**: Source code with docstrings

## 🆘 Support

For issues or questions, check the code documentation or create an issue in the repository.
