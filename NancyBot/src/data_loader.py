"""
Data loading and preparation module for NancyBot.

This module handles loading congressional trade data and stock price data.
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
import time
warnings.filterwarnings('ignore')


class CongressionalTradeLoader:
    """Load and process congressional trading data."""
    
    def __init__(self):
        """Initialize the trade loader."""
        self.trade_data = None
        self.price_data = {}
        
    def load_from_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load trade data from CSV file.
        
        Args:
            filepath: Path to CSV file with trade data
            
        Returns:
            DataFrame with trade data
        """
        try:
            df = pd.read_csv(filepath)
            
            # Convert date columns
            date_columns = ['trade_date', 'disclosure_date', 'filing_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            self.trade_data = df
            return df
        
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    def create_sample_data(self, 
                          politician: str = "Nancy Pelosi",
                          start_date: str = "2020-01-01",
                          end_date: str = "2026-03-01") -> pd.DataFrame:
        """
        Create sample trade data for testing purposes.
        
        This is a placeholder for demonstration. In production, replace with
        actual data from Capitol Trades, House Stock Watcher, or official sources.
        
        Args:
            politician: Name of politician
            start_date: Start date for sample data
            end_date: End date for sample data
            
        Returns:
            DataFrame with sample trade data
        """
        # Sample trades based on known public Pelosi trades
        sample_trades = [
            # 2020 Trades
            {'trade_date': '2020-01-15', 'ticker': 'AAPL', 'transaction_type': 'Purchase', 
             'amount_min': 500000, 'amount_max': 1000000},
            {'trade_date': '2020-03-20', 'ticker': 'MSFT', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            {'trade_date': '2020-06-15', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 250000, 'amount_max': 500000},
            
            # 2021 Trades
            {'trade_date': '2021-01-21', 'ticker': 'TSLA', 'transaction_type': 'Purchase',
             'amount_min': 500000, 'amount_max': 1000000},
            {'trade_date': '2021-03-19', 'ticker': 'GOOGL', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            {'trade_date': '2021-06-18', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            {'trade_date': '2021-11-22', 'ticker': 'NVDA', 'transaction_type': 'Sale',
             'amount_min': 1000000, 'amount_max': 5000000},
            
            # 2022 Trades
            {'trade_date': '2022-01-18', 'ticker': 'MSFT', 'transaction_type': 'Purchase',
             'amount_min': 500000, 'amount_max': 1000000},
            {'trade_date': '2022-07-26', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            {'trade_date': '2022-12-28', 'ticker': 'TSLA', 'transaction_type': 'Sale',
             'amount_min': 500000, 'amount_max': 1000000},
            
            # 2023 Trades
            {'trade_date': '2023-02-21', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 500000, 'amount_max': 1000000},
            {'trade_date': '2023-05-24', 'ticker': 'GOOGL', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            {'trade_date': '2023-11-22', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 5000000, 'amount_max': 25000000},
            
            # 2024 Trades
            {'trade_date': '2024-02-15', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            {'trade_date': '2024-07-17', 'ticker': 'AAPL', 'transaction_type': 'Purchase',
             'amount_min': 500000, 'amount_max': 1000000},
            {'trade_date': '2024-11-13', 'ticker': 'MSFT', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            
            # 2025 Trades  
            {'trade_date': '2025-01-22', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
            {'trade_date': '2025-06-18', 'ticker': 'TSLA', 'transaction_type': 'Purchase',
             'amount_min': 250000, 'amount_max': 500000},
            {'trade_date': '2025-11-19', 'ticker': 'GOOGL', 'transaction_type': 'Purchase',
             'amount_min': 500000, 'amount_max': 1000000},
            
            # 2026 Trades
            {'trade_date': '2026-01-27', 'ticker': 'NVDA', 'transaction_type': 'Purchase',
             'amount_min': 1000000, 'amount_max': 5000000},
        ]
        
        # Convert to DataFrame
        df = pd.DataFrame(sample_trades)
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        
        # Calculate disclosure date (30-45 days after trade)
        df['delay_days'] = np.random.randint(30, 46, size=len(df))
        df['disclosure_date'] = df['trade_date'] + pd.to_timedelta(df['delay_days'], unit='D')
        df['filing_date'] = df['disclosure_date']
        
        # Add amount midpoint
        df['amount_midpoint'] = (df['amount_min'] + df['amount_max']) / 2
        
        # Add amount range string
        df['amount_range'] = df.apply(
            lambda x: f"${x['amount_min']:,.0f} - ${x['amount_max']:,.0f}", 
            axis=1
        )
        
        # Add metadata
        df['representative'] = politician
        df['owner'] = 'Spouse'  # Paul Pelosi
        df['asset_type'] = 'Stock'
        df['party'] = 'Democrat'
        df['state'] = 'California'
        
        # Add trade_id
        df['trade_id'] = [f"TRADE_{i:06d}" for i in range(len(df))]
        
        # Reorder columns
        columns_order = [
            'trade_id', 'trade_date', 'disclosure_date', 'filing_date', 'delay_days',
            'ticker', 'transaction_type', 'amount_range', 'amount_min', 'amount_max',
            'amount_midpoint', 'asset_type', 'owner', 'representative', 'party', 'state'
        ]
        df = df[columns_order]
        
        self.trade_data = df
        return df
    
    def load_price_data(self, 
                       tickers: List[str],
                       start_date: str,
                       end_date: str,
                       batch_mode: bool = True,
                       delay: float = 3.0,
                       max_retries: int = 3) -> Dict[str, pd.DataFrame]:
        """
        Load historical price data for multiple tickers using yfinance.
        
        Uses batch downloading by default (recommended by yfinance to avoid rate limits).
        Falls back to individual downloads with retry logic if batch fails.
        
        Args:
            tickers: List of stock tickers
            start_date: Start date for price data
            end_date: End date for price data
            batch_mode: If True, download all tickers at once (recommended, default: True)
            delay: Delay in seconds between individual requests (default: 3.0)
            max_retries: Maximum retry attempts for failed downloads (default: 3)
            
        Returns:
            Dictionary mapping ticker to price DataFrame
        """
        price_data = {}
        
        print(f"Downloading price data for {len(tickers)} tickers...")
        
        if batch_mode:
            # Try batch download first (less likely to trigger rate limits)
            print("Using batch mode (recommended to avoid rate limits)...")
            try:
                # Download all tickers at once
                df_all = yf.download(
                    tickers, 
                    start=start_date, 
                    end=end_date,
                    group_by='ticker',
                    progress=False,
                    threads=True
                )
                
                # Process results
                if len(tickers) == 1:
                    # Single ticker returns differently
                    ticker = tickers[0]
                    if not df_all.empty:
                        price_data[ticker] = df_all
                        print(f"  ✓ {ticker} ({len(df_all)} days)")
                else:
                    # Multiple tickers
                    for ticker in tickers:
                        try:
                            if ticker in df_all.columns.get_level_values(0):
                                df = df_all[ticker].copy()
                                if not df.empty and not df['Close'].isna().all():
                                    price_data[ticker] = df
                                    print(f"  ✓ {ticker} ({len(df)} days)")
                                else:
                                    print(f"  ✗ {ticker} (no valid data)")
                        except Exception as e:
                            print(f"  ✗ {ticker} (error: {str(e)[:50]})")
                
                print(f"\nBatch download complete: {len(price_data)}/{len(tickers)} tickers")
                
            except Exception as e:
                print(f"\n⚠️  Batch download failed: {e}")
                print("Falling back to individual downloads with retry logic...\n")
                batch_mode = False
        
        if not batch_mode:
            # Individual downloads with retry logic
            print(f"Using individual mode with {delay}s delay and {max_retries} retries...")
            
            for i, ticker in enumerate(tickers, 1):
                success = False
                
                for attempt in range(max_retries):
                    try:
                        if attempt > 0:
                            # Exponential backoff
                            wait_time = delay * (2 ** attempt)
                            print(f"      Retry {attempt}/{max_retries} after {wait_time}s...")
                            time.sleep(wait_time)
                        
                        print(f"  [{i}/{len(tickers)}] {ticker}...", end=" ")
                        
                        df = yf.download(
                            ticker, 
                            start=start_date, 
                            end=end_date, 
                            progress=False
                        )
                        
                        if df.empty:
                            print(f"No data")
                            break
                        
                        # Flatten MultiIndex columns if needed
                        if isinstance(df.columns, pd.MultiIndex):
                            df.columns = df.columns.get_level_values(0)
                        
                        # Ensure we have required columns
                        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                        if all(col in df.columns for col in required_cols):
                            price_data[ticker] = df
                            print(f"✓ ({len(df)} days)")
                            success = True
                            break
                        else:
                            print(f"Missing columns")
                            break
                            
                    except Exception as e:
                        error_msg = str(e)
                        if 'Too Many Requests' in error_msg or 'Rate' in error_msg:
                            print(f"Rate limited!", end=" ")
                            if attempt < max_retries - 1:
                                continue
                            else:
                                print(f"\n      Failed after {max_retries} retries")
                        else:
                            print(f"Error: {error_msg[:50]}")
                            break
                
                # Add delay between tickers (except last one)
                if i < len(tickers) and success:
                    time.sleep(delay)
        
        self.price_data = price_data
        print(f"\n{'='*60}")
        print(f"Successfully loaded {len(price_data)}/{len(tickers)} tickers")
        print(f"{'='*60}")
        
        return price_data
    
    def calculate_trade_metrics(self) -> pd.DataFrame:
        """
        Calculate metrics for each trade including price movements and delays.
        
        Returns:
            DataFrame with enhanced trade data including metrics
        """
        if self.trade_data is None:
            raise ValueError("No trade data loaded. Call load_from_csv() or create_sample_data() first.")
        
        if not self.price_data:
            raise ValueError("No price data loaded. Call load_price_data() first.")
        
        df = self.trade_data.copy()
        
        # Initialize metric columns
        df['trade_price'] = np.nan
        df['disclosure_price'] = np.nan
        df['price_change_during_delay'] = np.nan
        df['price_change_pct_delay'] = np.nan
        
        for idx, trade in df.iterrows():
            ticker = trade['ticker']
            
            if ticker not in self.price_data:
                continue
            
            price_df = self.price_data[ticker]
            
            # Get trade date price (use close on trade date)
            try:
                trade_date = trade['trade_date']
                if trade_date in price_df.index:
                    df.loc[idx, 'trade_price'] = price_df.loc[trade_date, 'Close']
                else:
                    # Find nearest date after trade date
                    future_dates = price_df.index[price_df.index > trade_date]
                    if len(future_dates) > 0:
                        df.loc[idx, 'trade_price'] = price_df.loc[future_dates[0], 'Close']
            except:
                pass
            
            # Get disclosure date price
            try:
                disclosure_date = trade['disclosure_date']
                if disclosure_date in price_df.index:
                    df.loc[idx, 'disclosure_price'] = price_df.loc[disclosure_date, 'Close']
                else:
                    # Find nearest date after disclosure
                    future_dates = price_df.index[price_df.index > disclosure_date]
                    if len(future_dates) > 0:
                        df.loc[idx, 'disclosure_price'] = price_df.loc[future_dates[0], 'Close']
            except:
                pass
        
        # Calculate price changes during delay period
        df['price_change_during_delay'] = df['disclosure_price'] - df['trade_price']
        df['price_change_pct_delay'] = (df['price_change_during_delay'] / df['trade_price']) * 100
        
        return df
    
    def get_unique_tickers(self) -> List[str]:
        """
        Get unique tickers from trade data.
        
        Returns:
            List of unique ticker symbols
        """
        if self.trade_data is None:
            return []
        
        return sorted(self.trade_data['ticker'].unique().tolist())
    
    def filter_by_transaction_type(self, 
                                   transaction_type: str) -> pd.DataFrame:
        """
        Filter trades by transaction type.
        
        Args:
            transaction_type: 'Purchase', 'Sale', or 'Exchange'
            
        Returns:
            Filtered DataFrame
        """
        if self.trade_data is None:
            return pd.DataFrame()
        
        return self.trade_data[
            self.trade_data['transaction_type'] == transaction_type
        ].copy()
    
    def get_date_range(self) -> Tuple[datetime, datetime]:
        """
        Get date range of trade data.
        
        Returns:
            Tuple of (start_date, end_date)
        """
        if self.trade_data is None:
            return None, None
        
        return (
            self.trade_data['trade_date'].min(),
            self.trade_data['trade_date'].max()
        )
    
    def save_processed_data(self, filepath: str) -> None:
        """
        Save processed trade data to CSV.
        
        Args:
            filepath: Path to save CSV file
        """
        if self.trade_data is None:
            raise ValueError("No trade data to save")
        
        self.trade_data.to_csv(filepath, index=False)
        print(f"Saved trade data to {filepath}")


def get_next_market_open(ticker: str, 
                         date: datetime,
                         price_data: pd.DataFrame) -> Tuple[float, datetime]:
    """
    Get the next available market open price after a given date.
    
    Args:
        ticker: Stock ticker symbol
        date: Reference date
        price_data: DataFrame with price data
        
    Returns:
        Tuple of (open_price, actual_date)
    """
    # Find next available date
    future_dates = price_data.index[price_data.index > date]
    
    if len(future_dates) == 0:
        return None, None
    
    next_date = future_dates[0]
    open_price = price_data.loc[next_date, 'Open']
    
    return open_price, next_date


def calculate_forward_returns(ticker: str,
                              entry_date: datetime,
                              price_data: pd.DataFrame,
                              periods: List[int] = [1, 5, 20, 60]) -> Dict[str, float]:
    """
    Calculate forward returns for various holding periods.
    
    Args:
        ticker: Stock ticker symbol
        entry_date: Entry date
        price_data: DataFrame with price data
        periods: List of forward periods to calculate (in trading days)
        
    Returns:
        Dictionary of forward returns for each period
    """
    forward_returns = {}
    
    # Get entry price
    if entry_date not in price_data.index:
        future_dates = price_data.index[price_data.index > entry_date]
        if len(future_dates) == 0:
            return forward_returns
        entry_date = future_dates[0]
    
    entry_price = price_data.loc[entry_date, 'Close']
    entry_idx = price_data.index.get_loc(entry_date)
    
    for period in periods:
        exit_idx = entry_idx + period
        
        if exit_idx < len(price_data):
            exit_price = price_data.iloc[exit_idx]['Close']
            forward_return = (exit_price - entry_price) / entry_price
            forward_returns[f'{period}d'] = forward_return * 100
    
    return forward_returns
