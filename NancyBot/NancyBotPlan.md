# NancyBot - Congressional Trading Portfolio Strategy

**Date**: 2026-03-05  
**Author**: AI Assistant  
**Status**: Planning Phase  
**Target**: Replicate Nancy Pelosi (Paul Pelosi) trading portfolio with historical backtesting

---

## Executive Summary

NancyBot is a portfolio strategy that replicates trades disclosed by members of Congress, specifically focusing on Nancy Pelosi's (and her husband Paul Pelosi's) stock transactions. Due to mandatory disclosure requirements under the STOCK Act (2012), congressional trades are publicly available but with a reporting delay of up to 45 days. This project aims to:

1. **Historical Backtesting**: Test the viability of following these trades on historical data (2012-2026)
2. **Trade Execution Criteria**: Develop intelligent criteria for when to execute disclosed trades given the reporting delay
3. **Portfolio Management**: Implement position sizing, risk management, and exit strategies
4. **Performance Analysis**: Compare portfolio performance against S&P 500 benchmark

---

## Background & Context

### The STOCK Act (Stop Trading on Congressional Knowledge Act)
- **Enacted**: April 4, 2012
- **Purpose**: Prevent insider trading by government officials
- **Key Requirement**: Members of Congress must disclose stock trades within 30-45 days
- **Public Access**: Disclosures available through House and Senate ethics websites

### Why Nancy Pelosi?
- High-profile trades that often make headlines
- Husband Paul Pelosi is a venture capitalist and active investor
- Significant portfolio ($50M+ estimated)
- Trades often in tech stocks (AAPL, MSFT, NVDA, TSLA, etc.)
- Historical outperformance relative to market (controversial but documented)

### The Core Challenge: Reporting Delay
**Key Issue**: Trades are disclosed 30-45 days after execution, so we cannot copy them immediately.

**Questions to Answer**:
1. Do these trades still have alpha after the delay?
2. What criteria should trigger our trade execution?
3. Should we copy the full position, partial position, or skip it?
4. When should we exit?

---

## Data Sources

### Primary Data Source
**Option 1: Capitol Trades (capitoltrades.com)**
- Aggregates congressional trading data
- API or web scraping possible
- Historical data back to 2012

**Option 2: House Stock Watcher (housestockwatcher.com)**
- Community-driven congressional trade tracking
- Free data access
- Real-time updates

**Option 3: QuiverQuant API**
- Paid API for congressional trading data
- Clean, structured data
- Historical records

**Option 4: Manual Download from House/Senate Ethics**
- Official source but requires parsing PDF reports
- Most reliable but labor-intensive

### Secondary Data
- **Stock Prices**: `yfinance` for historical price data
- **Options Data**: If Paul Pelosi's options trades are included
- **Market Data**: S&P 500 (^GSPC) as benchmark

---

## Project Architecture

### Folder Structure
```
NancyBot/
├── data/                          # Raw and processed data
│   ├── raw/                       # Raw congressional trade data
│   ├── processed/                 # Cleaned and structured data
│   └── market/                    # Stock price data
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── 01_DataCollection.ipynb   # Data sourcing and cleaning
│   ├── 02_ExploratoryAnalysis.ipynb  # EDA on trade patterns
│   ├── 03_BacktestingSimple.ipynb    # Simple replication backtest
│   ├── 04_ExecutionCriteria.ipynb    # Develop trade criteria
│   └── 05_FullPortfolio.ipynb    # Complete portfolio strategy
├── src/                           # Python modules
│   ├── __init__.py
│   ├── data_loader.py            # Load and clean trade data
│   ├── trade_executor.py         # Trade execution logic
│   ├── portfolio.py              # Portfolio management
│   ├── backtester.py             # Backtesting engine
│   └── metrics.py                # Performance metrics
├── tests/                         # Unit tests
│   └── test_*.py
├── docs/                          # Additional documentation
│   └── API_NOTES.md              # Data source documentation
├── NancyBotPlan.md               # This file
└── requirements.txt              # Additional dependencies
```

---

## Implementation Plan

### Phase 1: Data Collection & Preparation (Week 1)

#### Step 1.1: Identify Data Source
- [ ] Research available data sources (Capitol Trades, House Stock Watcher, QuiverQuant)
- [ ] Select primary data source based on cost, quality, and ease of access
- [ ] Document API/scraping approach

#### Step 1.2: Collect Historical Trade Data
- [ ] Download Nancy Pelosi trade history (2012-2026)
- [ ] Parse trade data into structured format:
  ```python
  columns = [
      'trade_date',           # Date trade was executed
      'disclosure_date',      # Date trade was disclosed
      'ticker',               # Stock symbol
      'transaction_type',     # Buy/Sell
      'amount_range',         # Dollar range ($1k-$15k, $15k-$50k, etc.)
      'asset_type',           # Stock, Option, etc.
      'representative',       # Nancy Pelosi
      'owner',                # Self or Spouse (usually Spouse = Paul)
  ]
  ```
- [ ] Save to `/NancyBot/data/raw/pelosi_trades.csv`

#### Step 1.3: Download Stock Price Data
- [ ] Extract unique tickers from trade data
- [ ] Download historical price data using `yfinance`
- [ ] Handle corporate actions (splits, dividends)
- [ ] Save to `/NancyBot/data/market/`

#### Step 1.4: Data Cleaning
- [ ] Handle missing data
- [ ] Standardize ticker symbols (handle ticker changes)
- [ ] Convert amount ranges to midpoint estimates
- [ ] Calculate actual reporting delay for each trade
- [ ] Create analysis-ready dataset

**Deliverable**: `01_DataCollection.ipynb` with clean `processed/pelosi_trades_clean.csv`

---

### Phase 2: Exploratory Data Analysis (Week 1-2)

#### Step 2.1: Trade Pattern Analysis
- [ ] **Frequency**: How often does she trade?
- [ ] **Sectors**: Which sectors are preferred? (Tech, Finance, Healthcare)
- [ ] **Position Sizes**: Distribution of trade sizes
- [ ] **Hold Period**: How long between buy and sell?
- [ ] **Reporting Delay**: Average delay between trade and disclosure

#### Step 2.2: Performance Analysis
- [ ] Calculate forward returns for each disclosed trade:
  - 1-day forward return (from disclosure date)
  - 5-day forward return
  - 20-day forward return
  - 60-day forward return
- [ ] Compare to stock's historical average returns
- [ ] Identify if post-disclosure alpha exists

#### Step 2.3: Timing Analysis
- [ ] Analyze price movement between trade date and disclosure date
- [ ] Check if stocks trend up/down during delay period
- [ ] Identify if information is already "leaked" before disclosure

**Deliverable**: `02_ExploratoryAnalysis.ipynb` with key insights and visualizations

---

### Phase 3: Simple Replication Backtest (Week 2)

#### Step 3.1: Naive Strategy
**Rules**:
1. Buy stock on disclosure date at next open
2. Hold for fixed period (e.g., 60 days)
3. Sell at market
4. Equal weight all positions

**Implementation**:
```python
def simple_replication_strategy(trade_data, price_data):
    """
    Naive strategy: Buy on disclosure, hold 60 days, sell.
    """
    portfolio = Portfolio(initial_capital=100000)
    
    for idx, trade in trade_data.iterrows():
        if trade['transaction_type'] == 'Purchase':
            disclosure_date = trade['disclosure_date']
            ticker = trade['ticker']
            
            # Buy at next day's open
            entry_price = get_next_open(ticker, disclosure_date, price_data)
            position_size = calculate_position_size(portfolio, equal_weight=True)
            
            portfolio.buy(ticker, entry_price, position_size, disclosure_date)
            
            # Set exit date (60 days later)
            exit_date = disclosure_date + timedelta(days=60)
            exit_price = get_price(ticker, exit_date, price_data)
            
            portfolio.sell(ticker, exit_price, exit_date)
    
    return portfolio
```

#### Step 3.2: Performance Metrics
- [ ] Total return
- [ ] Annualized return
- [ ] Sharpe ratio
- [ ] Maximum drawdown
- [ ] Win rate
- [ ] Compare vs S&P 500

**Deliverable**: `03_BacktestingSimple.ipynb` with baseline performance

---

### Phase 4: Trade Execution Criteria Development (Week 3)

This is the **core innovation** of NancyBot. Given the disclosure delay, we need smart criteria for when to actually execute.

#### Step 4.1: Criteria Catalogue

**Criterion 1: Momentum Check**
- Only execute if stock has positive momentum since trade date
- Skip if stock has already run up significantly (>10% since trade date)

**Criterion 2: Volatility Filter**
- Check if stock volatility is within normal range
- Skip highly volatile periods (earnings, major news)

**Criterion 3: Relative Strength**
- Compare stock performance to sector/market
- Execute only if stock is showing relative strength

**Criterion 4: Technical Indicators**
- Check if stock is above key moving averages (50-day, 200-day)
- Confirm trend direction

**Criterion 5: Trade Size Signal**
- Larger trades (>$1M) may signal higher conviction
- Weight execution probability by trade size

**Criterion 6: Recent Activity**
- If multiple trades in same stock, increase conviction
- If selling after recent buying, be cautious

**Criterion 7: Options Activity**
- If options trades, check for bullish/bearish signals
- Options may signal short-term vs long-term view

#### Step 4.2: Scoring System
```python
def calculate_execution_score(trade, price_data, market_data):
    """
    Calculate score (0-100) for whether to execute trade.
    >70 = Execute, <30 = Skip, 30-70 = Partial position
    """
    score = 50  # Start neutral
    
    # Criterion 1: Price movement since trade date
    price_change = calculate_price_change(trade, price_data)
    if 0 < price_change < 0.10:
        score += 20  # Positive but not overextended
    elif price_change > 0.15:
        score -= 30  # Already run up too much
    
    # Criterion 2: Volatility
    volatility = calculate_volatility(trade['ticker'], price_data)
    if volatility < historical_average * 1.5:
        score += 10
    
    # Criterion 3: Relative strength
    relative_strength = calculate_relative_strength(trade, market_data)
    if relative_strength > 0:
        score += 15
    
    # Criterion 4: Technical indicators
    above_ma50 = check_above_ma(trade['ticker'], price_data, window=50)
    if above_ma50:
        score += 10
    
    # Criterion 5: Trade size
    if trade['amount_midpoint'] > 1_000_000:
        score += 15  # High conviction
    
    return max(0, min(100, score))  # Clamp to 0-100
```

#### Step 4.3: Optimization
- [ ] Test different threshold levels
- [ ] Optimize criterion weights
- [ ] Backtest performance with different scoring systems

**Deliverable**: `04_ExecutionCriteria.ipynb` with optimized criteria

---

### Phase 5: Full Portfolio Strategy (Week 4)

#### Step 5.1: Portfolio Management
- [ ] Position sizing (equal weight vs risk parity vs conviction-weighted)
- [ ] Maximum positions (e.g., max 20 stocks)
- [ ] Sector exposure limits
- [ ] Cash management

#### Step 5.2: Risk Management
- [ ] Stop-loss rules (e.g., -15% stop)
- [ ] Position limits (max 10% per stock)
- [ ] Correlation checks (avoid overconcentration)

#### Step 5.3: Exit Strategy
**Option A: Time-based**
- Hold for fixed period (30/60/90 days)

**Option B: Signal-based**
- Exit when Nancy sells (if disclosed)
- Exit on stop-loss or take-profit

**Option C: Technical-based**
- Exit on moving average cross
- Exit on RSI overbought

**Option D: Hybrid**
- Combination of above

#### Step 5.4: Complete Backtesting
```python
class NancyBotStrategy:
    def __init__(self, trade_data, price_data, config):
        self.trade_data = trade_data
        self.price_data = price_data
        self.config = config
        self.portfolio = Portfolio(initial_capital=100000)
    
    def run_backtest(self, start_date, end_date):
        """
        Run full backtest with execution criteria,
        portfolio management, and risk controls.
        """
        trades = self.trade_data[
            (self.trade_data['disclosure_date'] >= start_date) &
            (self.trade_data['disclosure_date'] <= end_date)
        ]
        
        for idx, trade in trades.iterrows():
            if trade['transaction_type'] == 'Purchase':
                # Calculate execution score
                score = calculate_execution_score(
                    trade, self.price_data, self.market_data
                )
                
                if score > self.config['execution_threshold']:
                    # Execute trade
                    self.execute_trade(trade, score)
                    
            elif trade['transaction_type'] == 'Sale':
                # Check if we hold this position
                if self.portfolio.has_position(trade['ticker']):
                    self.exit_position(trade)
        
        return self.portfolio.get_performance_metrics()
    
    def execute_trade(self, trade, score):
        """Execute trade with position sizing based on score."""
        position_size = self.calculate_position_size(trade, score)
        entry_price = self.get_entry_price(trade)
        self.portfolio.buy(
            trade['ticker'], 
            entry_price, 
            position_size, 
            trade['disclosure_date']
        )
    
    def exit_position(self, trade):
        """Exit position with defined exit strategy."""
        # Implementation based on exit strategy choice
        pass
```

**Deliverable**: `05_FullPortfolio.ipynb` with complete strategy

---

### Phase 6: Performance Analysis & Optimization (Week 5)

#### Step 6.1: Backtest Results
- [ ] Run backtest on full historical period (2012-2026)
- [ ] Calculate comprehensive metrics
- [ ] Compare vs benchmarks:
  - S&P 500
  - Buy-and-hold each stock
  - Equal-weight portfolio of all disclosed stocks

#### Step 6.2: Sensitivity Analysis
- [ ] Test different execution thresholds
- [ ] Test different holding periods
- [ ] Test different position sizing methods
- [ ] Test different stop-loss levels

#### Step 6.3: Visualization
- [ ] Cumulative returns chart
- [ ] Drawdown analysis
- [ ] Monthly/yearly returns heatmap
- [ ] Win/loss distribution
- [ ] Sector exposure over time

#### Step 6.4: Report Generation
- [ ] Create comprehensive performance report
- [ ] Document key findings
- [ ] Identify edge (if any)
- [ ] Recommendations for live trading

**Deliverable**: Final performance report and optimized strategy

---

## Technical Specifications

### Data Schema

#### Trade Data (`pelosi_trades_clean.csv`)
```python
{
    'trade_id': str,                    # Unique identifier
    'trade_date': datetime,             # Actual trade execution date
    'disclosure_date': datetime,        # Date disclosed to public
    'filing_date': datetime,            # Date filed with ethics office
    'delay_days': int,                  # Days between trade and disclosure
    'ticker': str,                      # Stock symbol
    'asset_description': str,           # Company name
    'transaction_type': str,            # Purchase, Sale, Exchange
    'amount_range': str,                # '$1,001 - $15,000', etc.
    'amount_min': float,                # Minimum dollar amount
    'amount_max': float,                # Maximum dollar amount
    'amount_midpoint': float,           # Midpoint estimate
    'asset_type': str,                  # Stock, Stock Option, etc.
    'owner': str,                       # Self, Spouse, Child
    'representative': str,              # 'Nancy Pelosi'
    'party': str,                       # 'Democrat'
    'state': str,                       # 'California'
}
```

#### Portfolio State
```python
{
    'date': datetime,
    'cash': float,
    'positions': {
        'AAPL': {
            'shares': float,
            'entry_price': float,
            'entry_date': datetime,
            'current_price': float,
            'market_value': float,
            'pnl': float,
            'pnl_pct': float,
        },
        # ... other positions
    },
    'total_value': float,
    'total_pnl': float,
}
```

### Key Functions

#### `src/data_loader.py`
```python
def load_pelosi_trades(filepath) -> pd.DataFrame:
    """Load and validate trade data."""

def load_price_data(tickers, start_date, end_date) -> Dict[str, pd.DataFrame]:
    """Load historical price data for multiple tickers."""

def calculate_delay(trade_data) -> pd.DataFrame:
    """Calculate reporting delay for each trade."""
```

#### `src/trade_executor.py`
```python
def calculate_execution_score(trade, price_data, config) -> float:
    """Calculate 0-100 score for trade execution."""

def should_execute_trade(score, threshold) -> bool:
    """Determine if trade should be executed."""

def calculate_position_size(portfolio, trade, score, config) -> float:
    """Calculate position size based on portfolio and score."""
```

#### `src/portfolio.py`
```python
class Portfolio:
    def __init__(self, initial_capital):
        """Initialize portfolio with starting capital."""
    
    def buy(self, ticker, price, quantity, date):
        """Execute buy order."""
    
    def sell(self, ticker, price, quantity, date):
        """Execute sell order."""
    
    def get_position(self, ticker):
        """Get current position in ticker."""
    
    def get_total_value(self, date, price_data):
        """Calculate total portfolio value."""
    
    def get_performance_metrics(self):
        """Calculate comprehensive performance metrics."""
```

#### `src/backtester.py`
```python
class Backtester:
    def __init__(self, strategy, trade_data, price_data, config):
        """Initialize backtester."""
    
    def run(self, start_date, end_date):
        """Run backtest over date range."""
    
    def calculate_metrics(self):
        """Calculate performance metrics."""
    
    def generate_report(self):
        """Generate performance report."""
```

#### `src/metrics.py`
```python
def calculate_returns(portfolio_history) -> pd.Series:
    """Calculate daily returns."""

def calculate_sharpe_ratio(returns, risk_free_rate=0.02) -> float:
    """Calculate annualized Sharpe ratio."""

def calculate_max_drawdown(portfolio_history) -> float:
    """Calculate maximum drawdown."""

def calculate_win_rate(trades) -> float:
    """Calculate percentage of winning trades."""

def calculate_profit_factor(trades) -> float:
    """Calculate profit factor (gross profit / gross loss)."""
```

---

## Risk Considerations

### Legal & Ethical
- **No insider information**: We only use publicly disclosed information
- **Legal to replicate**: Following disclosed trades is legal (no MNPI)
- **Reputational**: Be aware this is a controversial strategy

### Market Risk
- **Stale information**: 30-45 day delay means information may be priced in
- **Market conditions**: Strategy may work in bull markets but fail in bear markets
- **Liquidity**: Some positions may be in less liquid stocks

### Execution Risk
- **Slippage**: May not get exact entry prices, especially in volatile stocks
- **Options complexity**: Paul Pelosi's options trades are complex to replicate
- **Corporate actions**: Splits, mergers, bankruptcies

### Strategy Risk
- **Overfitting**: Risk of optimizing to historical data
- **Regime change**: Strategy may stop working if scrutiny increases
- **Small sample**: Limited number of trades may not be statistically significant

---

## Success Metrics

### Minimum Viable Success
- Beat S&P 500 by 1-2% annualized
- Sharpe ratio > 1.0
- Maximum drawdown < 30%
- Win rate > 55%

### Ideal Success
- Beat S&P 500 by 5%+ annualized
- Sharpe ratio > 1.5
- Maximum drawdown < 20%
- Win rate > 60%
- Consistent performance across market regimes

---

## Dependencies

### Python Packages
```txt
# Core
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0

# Data
yfinance>=0.2.0
requests>=2.31.0
beautifulsoup4>=4.12.0  # If web scraping needed

# Analysis
scipy>=1.10.0
statsmodels>=0.14.0

# Optional: Advanced analytics
ta-lib>=0.4.0  # Technical analysis library
quantstats>=0.0.59  # Portfolio analytics
```

### Data Requirements
- Historical congressional trade data (2012-2026)
- Daily stock price data for all tickers
- S&P 500 benchmark data

---

## Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Data Collection | Clean trade dataset + price data |
| 1-2 | Exploratory Analysis | EDA notebook with insights |
| 2 | Simple Backtest | Baseline strategy performance |
| 3 | Execution Criteria | Optimized trade execution rules |
| 4 | Full Portfolio | Complete strategy implementation |
| 5 | Analysis & Optimization | Final performance report |

**Total**: ~5 weeks for complete implementation and testing

---

## Next Steps

1. **Immediate**: Select data source for congressional trades
2. **Day 1-2**: Build data collection pipeline
3. **Day 3-5**: Clean data and perform EDA
4. **Week 2**: Implement and test simple replication strategy
5. **Week 3**: Develop and optimize execution criteria
6. **Week 4**: Build complete portfolio strategy
7. **Week 5**: Finalize and document results

---

## Open Questions

1. **Should we include options trades?** Paul Pelosi frequently trades options, which are more complex to replicate.
2. **How do we handle stock splits/mergers?** Need robust handling of corporate actions.
3. **Should we replicate sells?** Or just focus on purchases?
4. **What about other Congress members?** Could expand to other high-performing traders.
5. **Real-time implementation?** Do we want to build a system for ongoing live trading?

---

## References

- STOCK Act (2012): https://www.congress.gov/bill/112th-congress/senate-bill/2038
- House Ethics Disclosures: https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure
- Capitol Trades: https://www.capitoltrades.com
- QuiverQuant: https://www.quiverquant.com
- Academic paper on congressional trading: Ziobrowski et al. (2004) "Abnormal Returns from the Common Stock Investments of the U.S. Senate"

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-05
