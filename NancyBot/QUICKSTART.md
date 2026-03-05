# NancyBot Quick Start Guide

Get up and running with NancyBot in 5 minutes!

---

## Prerequisites

- Python 3.13+ (you have 3.13.3 ✅)
- Virtual environment activated
- Jupyter Lab or Jupyter Notebook

---

## Step 1: Setup Dependencies

```bash
# Navigate to NancyBot directory
cd /Users/johannes/Desktop/Finance/NancyBot

# Activate virtual environment (from parent directory)
source ../fin_env/bin/activate

# Install additional dependencies
pip install -r requirements.txt
```

**Dependencies installed**:
- pandas, numpy, matplotlib (already installed)
- yfinance (already installed)
- seaborn - Enhanced visualizations
- scipy, statsmodels - Statistical analysis
- requests, beautifulsoup4 - For future data scraping

---

## Step 2: Run Data Collection

```bash
# Start Jupyter Lab
jupyter lab

# Open and run: notebooks/01_DataCollection.ipynb
```

**What it does**:
1. Creates sample Nancy Pelosi trade data (20 trades, 2020-2026)
2. Downloads historical stock prices for all tickers
3. Calculates price movements during delay periods
4. Computes forward returns (1d, 5d, 20d, 60d)
5. Generates visualizations
6. Saves cleaned data to `/data` folder

**Expected output files**:
- `data/pelosi_trades_clean.csv`
- `data/pelosi_purchases_with_returns.csv`
- `data/price_data_summary.csv`

**Time**: ~2-3 minutes

---

## Step 3: Run Exploratory Analysis

```bash
# Open and run: notebooks/02_ExploratoryAnalysis.ipynb
```

**What it does**:
1. Loads processed trade data
2. Analyzes trading frequency over time
3. Identifies stock preferences (NVDA, MSFT, GOOGL, AAPL)
4. Examines trade size distribution
5. Studies reporting delay patterns
6. Calculates performance metrics
7. Compares to S&P 500 benchmark

**Key insights to discover**:
- Heavy tech stock concentration
- 30-45 day reporting delays
- Price movement during delay period
- Post-disclosure alpha potential

**Time**: ~3-5 minutes

---

## Step 4: Run Simple Backtest

```bash
# Open and run: notebooks/03_BacktestingSimple.ipynb
```

**What it does**:
1. Implements naive replication strategy
2. Tests 3 hold periods (30, 60, 90 days)
3. Simulates portfolio with $100K starting capital
4. Tracks all trades and positions
5. Calculates comprehensive performance metrics
6. Compares strategies and visualizes equity curves

**Expected results**:
- Total return: 10-30% (sample data dependent)
- Win rate: 55-65%
- Sharpe ratio: 0.5-1.0
- Benchmark comparison vs SPY

**Time**: ~5-7 minutes

---

## Project Structure

```
NancyBot/
├── 📄 NancyBotPlan.md              # 22KB comprehensive plan
├── 📄 IMPLEMENTATION_STATUS.md      # Current status (you are here)
├── 📄 README.md                     # Project overview
├── 📄 requirements.txt              # Python dependencies
│
├── 📂 src/                          # Python modules
│   ├── data_loader.py              # Data loading & processing
│   ├── portfolio.py                # Portfolio management
│   ├── metrics.py                  # Performance metrics
│   └── __init__.py
│
├── 📂 notebooks/                    # Jupyter notebooks
│   ├── 01_DataCollection.ipynb     # Phase 1 ✅
│   ├── 02_ExploratoryAnalysis.ipynb # Phase 2 ✅
│   ├── 03_BacktestingSimple.ipynb  # Phase 3 ✅
│   ├── 04_ExecutionCriteria.ipynb  # Phase 4 (TODO)
│   └── 05_FullPortfolio.ipynb      # Phase 5 (TODO)
│
├── 📂 data/                         # Data files (created by notebooks)
│   ├── pelosi_trades_clean.csv
│   ├── pelosi_purchases_with_returns.csv
│   └── price_data_summary.csv
│
├── 📂 docs/                         # Documentation
│   └── API_NOTES.md                # Data source research
│
└── 📂 tests/                        # Unit tests (TODO)
```

---

## Quick Commands

### Start Jupyter Lab
```bash
cd /Users/johannes/Desktop/Finance/NancyBot
source ../fin_env/bin/activate
jupyter lab
```

### Run All Notebooks (Non-Interactive)
```bash
# Data Collection
jupyter nbconvert --execute --to notebook --inplace notebooks/01_DataCollection.ipynb

# Exploratory Analysis
jupyter nbconvert --execute --to notebook --inplace notebooks/02_ExploratoryAnalysis.ipynb

# Simple Backtest
jupyter nbconvert --execute --to notebook --inplace notebooks/03_BacktestingSimple.ipynb
```

### Check Installation
```bash
python -c "import pandas, numpy, matplotlib, yfinance, seaborn, scipy; print('All dependencies OK!')"
```

---

## Understanding the Sample Data

The sample data includes **20 realistic trades** based on publicly known Nancy Pelosi (Paul Pelosi) transactions:

**Tickers**: AAPL, MSFT, NVDA, GOOGL, TSLA  
**Date Range**: 2020-2026  
**Trade Sizes**: $250K - $5M  
**Transaction Types**: Purchases and Sales  

**Example Trade**:
```
Trade Date:      2023-11-22
Disclosure Date: 2024-01-05 (45 days later)
Ticker:          NVDA
Type:            Purchase
Amount:          $5M - $25M (midpoint: $15M)
```

**Note**: This is sample data for demonstration. For production use, integrate with:
- Capitol Trades API
- House Stock Watcher
- QuiverQuant
- Official House Ethics disclosures

---

## Common Issues & Solutions

### Issue: "Module not found"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: "No data folder"
```bash
# Solution: Create data directory
mkdir -p data
```

### Issue: "yfinance download fails"
```bash
# Solution: Check internet connection and try again
# yfinance occasionally has rate limiting
```

### Issue: "Kernel crashes in Jupyter"
```bash
# Solution: Restart kernel and clear outputs
# Jupyter → Kernel → Restart & Clear Output
```

---

## Next Steps After Quick Start

### 1. Analyze Results
- Review equity curves
- Examine closed trades
- Compare hold periods
- Identify best performing strategy

### 2. Customize Parameters
- Change `initial_capital`
- Adjust `max_positions`
- Test different `hold_days`
- Modify position sizing

### 3. Integrate Real Data
- Research Capitol Trades API
- Implement web scraping
- Download historical disclosures
- Expand ticker universe

### 4. Implement Phase 4
- Build execution criteria scoring system
- Add momentum filters
- Implement technical indicators
- Optimize thresholds

### 5. Complete Phase 5
- Add risk management
- Implement stop-loss
- Dynamic position sizing
- Multiple exit strategies

---

## Key Metrics to Watch

### Returns
- **Total Return**: Overall portfolio gain/loss
- **Annualized Return**: Extrapolated yearly return
- **Alpha**: Outperformance vs S&P 500

### Risk
- **Volatility**: Standard deviation of returns
- **Sharpe Ratio**: Risk-adjusted return (>1.0 is good)
- **Max Drawdown**: Largest peak-to-trough decline

### Trading
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit / Gross loss (>1.0 is profitable)
- **Expectancy**: Average profit per trade

---

## Tips for Best Results

### 1. Run Notebooks Sequentially
Always run in order: 01 → 02 → 03

### 2. Check Data Quality
Verify that price data downloads successfully for all tickers

### 3. Understand the Delay
Remember: We see trades 30-45 days AFTER execution

### 4. Benchmark Everything
Always compare to S&P 500 (SPY) buy-and-hold

### 5. Iterate and Improve
- Start with simple strategy (Phase 3)
- Add intelligence (Phase 4)
- Optimize (Phase 5)

---

## Resources

### Documentation
- `NancyBotPlan.md` - Comprehensive implementation plan
- `IMPLEMENTATION_STATUS.md` - Current progress status
- `README.md` - Project overview
- `docs/API_NOTES.md` - Data source research

### Code
- `src/data_loader.py` - ~500 lines
- `src/portfolio.py` - ~400 lines
- `src/metrics.py` - ~340 lines

### External Resources
- [STOCK Act (2012)](https://www.congress.gov/bill/112th-congress/senate-bill/2038)
- [Capitol Trades](https://www.capitoltrades.com)
- [House Ethics Disclosures](https://disclosures-clerk.house.gov)

---

## Getting Help

### Check the Plan
See `NancyBotPlan.md` for detailed explanations

### Review the Code
All modules have comprehensive docstrings

### Run in Debug Mode
Use Jupyter's debugger to step through code

### Check Outputs
All notebooks have extensive print statements

---

## Success Checklist

After running all notebooks, you should have:

- [ ] Clean trade data in `/data` folder
- [ ] Price data for all tickers
- [ ] Comprehensive trade analysis
- [ ] Multiple backtest results
- [ ] Performance comparison vs S&P 500
- [ ] Equity curve visualizations
- [ ] Trade-by-trade breakdown

---

**Ready to Go!** 🚀

You now have a fully functional congressional trading analysis and backtesting system. The foundation is solid for Phase 4 (smart execution criteria) and Phase 5 (full portfolio strategy with risk management).

Good luck and happy trading! 📈
