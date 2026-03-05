# Data Source API Notes

This document tracks research and notes on data sources for congressional trading data.

## Data Source Options

### 1. Capitol Trades (capitoltrades.com)
- **Status**: To be investigated
- **Pros**: Clean UI, aggregated data
- **Cons**: May require web scraping, unclear on API availability
- **Cost**: Unknown
- **Historical Data**: Appears to have data back to 2012

### 2. House Stock Watcher (housestockwatcher.com)
- **Status**: To be investigated  
- **Pros**: Community-driven, free
- **Cons**: Data quality uncertain
- **Cost**: Free
- **Historical Data**: Unknown coverage

### 3. QuiverQuant (quiverquant.com)
- **Status**: To be investigated
- **Pros**: Professional API, clean data
- **Cons**: Paid service
- **Cost**: Subscription-based (pricing TBD)
- **Historical Data**: Likely comprehensive

### 4. Official House/Senate Ethics Disclosures
- **Status**: To be investigated
- **Source**: https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure
- **Pros**: Official source, most reliable
- **Cons**: PDF parsing required, labor-intensive
- **Cost**: Free
- **Historical Data**: Complete since STOCK Act (2012)

## Research Tasks

- [ ] Check Capitol Trades for API or scraping feasibility
- [ ] Test House Stock Watcher data quality
- [ ] Investigate QuiverQuant pricing
- [ ] Research existing Python libraries for congressional trade data
- [ ] Test official disclosure portal for automated access

## Data Requirements

### Minimum Required Fields
- Trade execution date
- Disclosure date
- Ticker symbol
- Transaction type (Buy/Sell)
- Amount range

### Desired Additional Fields
- Asset type (Stock vs Options)
- Owner (Self vs Spouse)
- Filing date
- Asset description

---

**Last Updated**: 2026-03-05
