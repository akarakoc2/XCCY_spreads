# XCCY Spreads Analyzer

A comprehensive, modular toolkit for calculating, analyzing, and visualizing cross-currency (XCCY) spreads with advanced OAS (Option-Adjusted Spread) curve fitting using Nelson-Siegel-Svensson methodology.

## 🎯 Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for calculations, data handling, and visualization
- **Nelson-Siegel-Svensson Curve Fitting**: Bloomberg NIA-style curve fitting for OAS spreads
- **Flexible Data Processing**: Support for CSV, Excel, and JSON data formats
- **Advanced Visualizations**: Professional-grade plots with customizable styling
- **Statistical Analysis**: Built-in goodness-of-fit metrics (R², RMSE, MAE)
- **Extensible Design**: Easy to add new calculation methods and visualization types

## 📁 Project Structure

```
XCCY_spreads/
│
├── src/                          # Source code modules
│   ├── engine/                   # Calculation engine
│   │   ├── calculator.py         # Spread calculations
│   │   ├── curve_fitting.py      # NSS and curve fitting models
│   │   └── models.py             # Data models
│   │
│   ├── data/                     # Data handling
│   │   ├── loader.py             # Data loading utilities
│   │   ├── processor.py          # Data processing & transformation
│   │   └── exporter.py           # Data export utilities
│   │
│   └── visualization/            # Visualization components
│       ├── plotter.py            # General plotting utilities
│       ├── oas_plotter.py        # OAS-specific plotting
│       └── dashboard.py          # Dashboard creation
│
├── config/                       # Configuration files
│   ├── config.json               # Application settings
│   └── __init__.py               # Config manager
│
├── tests/                        # Unit tests (future)
├── output/                       # Generated outputs
├── main.py                       # Main application entry
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/akarakoc2/XCCY_spreads.git
cd XCCY_spreads
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

Run the OAS curve analysis on your bond data:

```bash
python main.py
```

This will:
- Load data from `Data.xlsx`
- Filter bonds by OAS and duration criteria
- Fit Nelson-Siegel-Svensson curve
- Display fitted parameters and goodness-of-fit metrics
- Save visualization to `output/oas_curve_nss.png`

## 📊 Usage Examples

### 1. OAS Curve Fitting

```python
from src.data import DataLoader
from src.visualization import OASCurvePlotter

# Load data
loader = DataLoader()
df = loader.load_excel("Data.xlsx")

# Extract bond data
durations = df['bid_years_to_wkout'].values
oas_values = df['oas'].values

# Create and plot OAS curve
plotter = OASCurvePlotter()
fig = plotter.plot_oas_curve_with_nss(
    durations=durations,
    oas_values=oas_values,
    filter_params={'max_oas': 150, 'min_duration': 1},
    save_path='output/oas_curve.png'
)
plotter.show()
```

### 2. Spread Calculations

```python
from src.engine import SpreadCalculator, CurrencyPair

# Initialize calculator
calculator = SpreadCalculator()

# Create currency pair
pair = CurrencyPair("USD", "EUR")

# Calculate spread
spread = calculator.calculate_spread(
    currency_pair=pair,
    forward_rate=1.12,
    spot_rate=1.10,
    time_period=1.0
)

print(f"Spread: {spread.basis_points:.2f} bps")
```

### 3. Data Processing

```python
from src.data import DataProcessor

processor = DataProcessor()

# Calculate moving average
df['ma_7'] = processor.calculate_moving_average(df, 'spread', window=7)

# Resample time series
df_resampled = processor.resample_timeseries(
    df, 
    date_column='date',
    frequency='W',  # Weekly
    aggregation='mean'
)
```

### 4. Custom Visualizations

```python
from src.visualization import SpreadPlotter

plotter = SpreadPlotter()

# Time series plot
plotter.plot_time_series(
    df=df,
    x_column='date',
    y_columns=['spread_usd_eur', 'spread_usd_gbp'],
    title='XCCY Spread Analysis',
    save_path='output/spread_timeseries.png'
)

# Distribution plot
plotter.plot_distribution(
    df=df,
    column='spread_bps',
    title='Spread Distribution',
    save_path='output/spread_dist.png'
)
```

## 🔧 Configuration

Customize application behavior via `config/config.json`:

```json
{
    "oas_analysis": {
        "max_oas_filter": 150,
        "min_duration_filter": 1,
        "curve_fitting_method": "nelson_siegel_svensson"
    },
    "visualization": {
        "figure_size": [12, 7],
        "dpi": 300,
        "save_plots": true
    }
}
```

Access configuration in code:

```python
from config import get_config

config = get_config()
max_oas = config.get('oas_analysis.max_oas_filter', 150)
```

## 📈 Nelson-Siegel-Svensson Model

The NSS model is a parametric approach for fitting yield curves:

**NSS(t) = β₀ + β₁ · f₁(t,τ₁) + β₂ · f₂(t,τ₁) + β₃ · f₂(t,τ₂)**

Where:
- **β₀**: Level (long-term rate)
- **β₁**: Slope (short-term component)
- **β₂**: Curvature (medium-term component)
- **β₃**: Second curvature (additional flexibility)
- **τ₁, τ₂**: Time decay parameters

This model is used by Bloomberg for their NIA curves and provides smooth, economically interpretable curve fits.

## 📦 Module Overview

### Engine Module
- `SpreadCalculator`: Core calculation engine for XCCY spreads
- `NelsonSiegelSvensson`: NSS curve fitting implementation
- `CurveFitter`: Additional curve fitting methods (PCHIP, etc.)
- `CurrencyPair` & `SpreadData`: Data models

### Data Module
- `DataLoader`: Load data from CSV, Excel, JSON
- `DataProcessor`: Clean, transform, and process data
- `DataExporter`: Export results to various formats

### Visualization Module
- `SpreadPlotter`: General-purpose plotting utilities
- `OASCurvePlotter`: Specialized OAS curve visualization
- `Dashboard`: Multi-panel dashboard creation

## 🧪 Testing

(Tests to be implemented)

```bash
pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**akarakoc2**

## 🙏 Acknowledgments

- Nelson-Siegel-Svensson model based on Bloomberg's NIA methodology
- Inspired by quantitative finance best practices

---

**Note**: This tool is designed to be generally applicable for spread analysis across different asset classes and currency pairs. The modular architecture allows easy extension for specific use cases.
Quant Tool to analyze the cross currency spreads.
