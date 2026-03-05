# NancyBot - Congressional Trading Portfolio Strategy

A quantitative trading strategy that replicates Nancy Pelosi's (Paul Pelosi's) disclosed stock trades with intelligent execution criteria to account for reporting delays.

## Overview

NancyBot aims to test whether following congressional trading disclosures can generate alpha, specifically focusing on Nancy Pelosi's trades which have historically shown strong performance. The core challenge is the 30-45 day reporting delay mandated by the STOCK Act.

## Project Status

🟡 **Planning Phase** - Data collection and strategy design in progress

## Quick Start

### Prerequisites
- Python 3.13+
- Virtual environment (`fin_env` in parent directory)
- Jupyter Lab/Notebook

### Installation

```bash
# Activate virtual environment
source ../fin_env/bin/activate

# Install additional dependencies
pip install -r requirements.txt
```

### Project Structure

```
NancyBot/
├── data/              # Trade and market data
├── notebooks/         # Jupyter notebooks for analysis
├── src/              # Python source code
├── tests/            # Unit tests
├── docs/             # Documentation
├── NancyBotPlan.md   # Comprehensive project plan
└── requirements.txt  # Python dependencies
```

## Key Features (Planned)

- **Historical Backtesting**: Test strategy on 2012-2026 data
- **Smart Execution Criteria**: Determine when to execute delayed trades
- **Portfolio Management**: Position sizing and risk controls
- **Performance Analytics**: Comprehensive metrics vs S&P 500

## Documentation

See [NancyBotPlan.md](./NancyBotPlan.md) for complete implementation plan.

## Legal Notice

This project uses only publicly disclosed information available under the STOCK Act (2012). All trades are disclosed 30-45 days after execution and are publicly available. This strategy does not use or rely on any material non-public information (MNPI).

## License

See parent project license.

---

**Last Updated**: 2026-03-05
