# Agent Guidelines for Finance Project

## Project Overview

This is a Python-based financial analysis project using Jupyter notebooks for developing and backtesting trading strategies. The project focuses on quantitative finance, stock market analysis, and algorithmic trading strategy development.

## Environment Setup

### Python Virtual Environment
```bash
# Activate the virtual environment
source fin_env/bin/activate

# Install dependencies
pip install -r requirements.txt  # If exists

# Deactivate when done
deactivate
```

### Required Libraries
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Data visualization
- `yfinance` - Yahoo Finance data fetching

## Running Code

### Jupyter Notebooks
```bash
# Start Jupyter Lab/Notebook
jupyter lab
# or
jupyter notebook

# Run specific notebook (non-interactive)
jupyter nbconvert --execute --to notebook Basics.ipynb
jupyter nbconvert --execute --to notebook SimpleStrategy.ipynb
```

### Python Scripts
```bash
# Run Python files directly
python script_name.py

# Run with virtual environment
./fin_env/bin/python script_name.py
```

### No Traditional Test Framework Detected
This project appears to use Jupyter notebooks for analysis rather than traditional unit tests. Validation is done through visual analysis and metrics computation.

## Code Style Guidelines

### Python Conventions

#### Import Organization
```python
# Standard library imports first
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Third-party imports
import yfinance as yf

# Local imports (if any)
# from local_module import function
```

#### Naming Conventions
- **Variables**: `snake_case` (e.g., `apple_data`, `close_prices`, `fast_window`)
- **Functions**: `snake_case` (e.g., `ma_crossover_strategy()`, `generate_metric()`)
- **Constants**: `UPPER_CASE` (e.g., `MA5`, `MA20`)
- **DataFrames**: descriptive names with `_data` or `_df` suffix (e.g., `apple_data`, `strategy_data`)

#### Formatting Standards
- **Line length**: Aim for 88-100 characters (Black formatter standard)
- **Indentation**: 4 spaces (Python standard)
- **String quotes**: Single quotes `'` preferred, but be consistent
- **Trailing commas**: Use in multi-line structures for cleaner diffs

#### Comments and Documentation
```python
def function_name(arg1, arg2) -> return_type:
    """
    Brief description of function purpose.
    
    Args:
        arg1 (type): Description of first argument.
        arg2 (type): Description of second argument.
        
    Returns:
        return_type: Description of return value.
    """
    # Implementation with inline comments for complex logic
    pass
```

### Data Analysis Conventions

#### DataFrame Operations
```python
# Flatten MultiIndex columns after yfinance download
data.columns = data.columns.get_level_values(0)

# Use descriptive column names
df['Fast_MA'] = df['Close'].rolling(window=5).mean()
df['Slow_MA'] = df['Close'].rolling(window=20).mean()

# Clean up NaN values explicitly
df.dropna(inplace=True)
```

#### Plotting Standards
```python
# Use descriptive titles and labels
plt.title('Clear Description of What Is Plotted')
plt.ylabel('Unit/Measurement')
plt.xlabel('Time/Category')
plt.legend()

# Set figure size for readability
plt.figure(figsize=(12, 6))

# Use alpha for overlapping plots
plt.plot(data, alpha=0.6)
```

### Financial Calculations

#### Returns Calculation
```python
# Percentage returns
df['Returns'] = df['Close'].pct_change()

# Cumulative returns
df['Cumulative_Returns'] = (1 + df['Returns']).cumprod() - 1
```

#### Annualization
```python
# Annualized return (252 trading days)
annualized_return = (1 + total_return) ** (1 / years) - 1

# Annualized volatility
annualized_volatility = daily_volatility * np.sqrt(252)
```

## Error Handling

### Data Fetching
```python
try:
    stock_data = yf.download(ticker, start='2020-01-01', end='2026-01-01')
    stock_data.columns = stock_data.columns.get_level_values(0)
except Exception as e:
    print(f"Error fetching {ticker}: {e}")
    continue
```

### Division by Zero
```python
# Use conditional expressions
sharpe_ratio = (return - risk_free) / volatility if volatility != 0 else np.nan
```

## Git Workflow

### Ignored Files (from .gitignore)
- `__pycache__/` - Python cache directories
- `.env` - Environment variables
- `.DS_Store` - macOS system files
- `venv/` - Virtual environment directories
- `*.csv` - Data files (likely excluded due to size)

### Commit Messages
```bash
# Use descriptive commit messages
git commit -m "Add moving average crossover strategy"
git commit -m "Fix annualized return calculation"
git commit -m "Update visualization for portfolio comparison"
```

## Best Practices

### Strategy Development
1. **Copy DataFrame**: Always work on copies to avoid modifying original data
   ```python
   df = data.copy()
   ```

2. **Signal Shifting**: Account for look-ahead bias by shifting signals
   ```python
   df['Strategy_Returns'] = df['Signal'].shift(2) * df['Open_Returns']
   ```

3. **Validation**: Always compute and display performance metrics
   - Total and annualized returns
   - Volatility (risk measure)
   - Sharpe ratio (risk-adjusted return)
   - Maximum drawdown (if applicable)

### Visualization
1. Use color schemes that are colorblind-friendly
2. Include legends for multi-line plots
3. Use grid lines for easier reading (`plt.grid(alpha=0.3)`)
4. Format percentages properly using `PercentFormatter(1)`

### Performance
1. Avoid unnecessary recalculation in loops
2. Use vectorized operations (pandas/numpy) instead of loops
3. Cache expensive operations when possible

## Common Patterns

### Strategy Backtesting Template
```python
def strategy_function(data, param1, param2):
    """Strategy implementation."""
    df = data.copy()
    
    # Calculate indicators
    df['Indicator'] = calculate_indicator(df, param1)
    
    # Generate signals
    df['Signal'] = generate_signals(df, param2)
    df['Entry_Exit'] = df['Signal'].diff()
    
    # Calculate returns
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Signal'].shift(2) * df['Returns']
    
    # Cumulative returns
    df['Cumulative_Market'] = (1 + df['Returns']).cumprod() - 1
    df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod() - 1
    
    return df.dropna()
```

### Metrics Computation
```python
def generate_metrics(df):
    """Calculate performance metrics."""
    days = len(df)
    years = days / 252
    
    total_return = df['Cumulative_Returns'].iloc[-1]
    annualized_return = (1 + total_return) ** (1 / years) - 1
    volatility = df['Returns'].std() * np.sqrt(252)
    
    return {
        'Total Return': total_return,
        'Annualized Return': annualized_return,
        'Volatility': volatility,
    }
```

## Troubleshooting

### Common Issues
1. **MultiIndex columns after yfinance**: Always flatten with `.get_level_values(0)`
2. **NaN values**: Use `.dropna()` or `.fillna()` appropriately
3. **Look-ahead bias**: Always shift signals before calculating returns
4. **RuntimeWarning in calculations**: Handle negative values in power operations

### Debugging
```python
# Display DataFrame info
print(df.info())
print(df.head())
print(df.describe())

# Check for NaN values
print(df.isnull().sum())

# Verify calculations
print(f"Debug: {variable_name}")
```

---

**Last Updated**: 2026-02-24
**Python Version**: 3.13.3
**Primary Dependencies**: pandas, numpy, matplotlib, yfinance
