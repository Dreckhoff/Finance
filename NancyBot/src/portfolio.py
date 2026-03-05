"""
Portfolio management module for NancyBot.

Handles position tracking, cash management, and trade execution.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Position:
    """Represents a single stock position."""
    ticker: str
    shares: float
    entry_price: float
    entry_date: datetime
    current_price: float = 0.0
    
    @property
    def market_value(self) -> float:
        """Current market value of position."""
        return self.shares * self.current_price
    
    @property
    def cost_basis(self) -> float:
        """Total cost basis of position."""
        return self.shares * self.entry_price
    
    @property
    def pnl(self) -> float:
        """Profit/loss in dollars."""
        return self.market_value - self.cost_basis
    
    @property
    def pnl_pct(self) -> float:
        """Profit/loss in percentage."""
        if self.cost_basis == 0:
            return 0.0
        return (self.pnl / self.cost_basis) * 100
    
    def to_dict(self) -> Dict:
        """Convert position to dictionary."""
        return {
            'ticker': self.ticker,
            'shares': self.shares,
            'entry_price': self.entry_price,
            'entry_date': self.entry_date,
            'current_price': self.current_price,
            'cost_basis': self.cost_basis,
            'market_value': self.market_value,
            'pnl': self.pnl,
            'pnl_pct': self.pnl_pct
        }


class Portfolio:
    """
    Portfolio manager for tracking positions, cash, and performance.
    """
    
    def __init__(self, initial_capital: float = 100000):
        """
        Initialize portfolio.
        
        Args:
            initial_capital: Starting cash amount
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.trade_history: List[Dict] = []
        self.equity_curve: List[Dict] = []
        
    def buy(self, 
            ticker: str,
            price: float,
            shares: float,
            date: datetime,
            notes: str = "") -> bool:
        """
        Execute a buy order.
        
        Args:
            ticker: Stock ticker
            price: Purchase price per share
            shares: Number of shares to buy
            date: Trade date
            notes: Optional notes about the trade
            
        Returns:
            True if successful, False otherwise
        """
        cost = price * shares
        
        # Check if we have enough cash
        if cost > self.cash:
            print(f"Insufficient cash for {ticker}. Need ${cost:,.2f}, have ${self.cash:,.2f}")
            return False
        
        # Deduct cash
        self.cash -= cost
        
        # Add or update position
        if ticker in self.positions:
            # Average up
            existing = self.positions[ticker]
            total_shares = existing.shares + shares
            avg_price = (existing.cost_basis + cost) / total_shares
            
            self.positions[ticker] = Position(
                ticker=ticker,
                shares=total_shares,
                entry_price=avg_price,
                entry_date=existing.entry_date,  # Keep original entry date
                current_price=price
            )
        else:
            # New position
            self.positions[ticker] = Position(
                ticker=ticker,
                shares=shares,
                entry_price=price,
                entry_date=date,
                current_price=price
            )
        
        # Record trade
        self.trade_history.append({
            'date': date,
            'action': 'BUY',
            'ticker': ticker,
            'shares': shares,
            'price': price,
            'value': cost,
            'cash_after': self.cash,
            'notes': notes
        })
        
        return True
    
    def sell(self,
             ticker: str,
             price: float,
             shares: Optional[float] = None,
             date: datetime = None,
             notes: str = "") -> bool:
        """
        Execute a sell order.
        
        Args:
            ticker: Stock ticker
            price: Sale price per share
            shares: Number of shares to sell (None = sell all)
            date: Trade date
            notes: Optional notes about the trade
            
        Returns:
            True if successful, False otherwise
        """
        if ticker not in self.positions:
            print(f"No position in {ticker} to sell")
            return False
        
        position = self.positions[ticker]
        
        # Determine shares to sell
        shares_to_sell = shares if shares is not None else position.shares
        
        if shares_to_sell > position.shares:
            print(f"Cannot sell {shares_to_sell} shares of {ticker}, only have {position.shares}")
            return False
        
        # Calculate proceeds
        proceeds = price * shares_to_sell
        self.cash += proceeds
        
        # Calculate P&L for this trade
        cost_basis = position.entry_price * shares_to_sell
        pnl = proceeds - cost_basis
        pnl_pct = (pnl / cost_basis) * 100 if cost_basis > 0 else 0
        
        # Update or remove position
        if shares_to_sell >= position.shares:
            # Close entire position
            del self.positions[ticker]
        else:
            # Partial sale
            position.shares -= shares_to_sell
        
        # Record trade
        self.trade_history.append({
            'date': date,
            'action': 'SELL',
            'ticker': ticker,
            'shares': shares_to_sell,
            'price': price,
            'value': proceeds,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'cash_after': self.cash,
            'notes': notes
        })
        
        return True
    
    def update_prices(self, prices: Dict[str, float], date: datetime = None):
        """
        Update current prices for all positions.
        
        Args:
            prices: Dictionary mapping ticker to current price
            date: Current date
        """
        for ticker in self.positions:
            if ticker in prices:
                self.positions[ticker].current_price = prices[ticker]
        
        # Record equity snapshot
        if date:
            self.equity_curve.append({
                'date': date,
                'cash': self.cash,
                'positions_value': self.get_positions_value(),
                'total_value': self.get_total_value(),
                'returns': self.get_total_return()
            })
    
    def get_position(self, ticker: str) -> Optional[Position]:
        """Get position for a ticker."""
        return self.positions.get(ticker)
    
    def has_position(self, ticker: str) -> bool:
        """Check if we have a position in ticker."""
        return ticker in self.positions
    
    def get_positions_value(self) -> float:
        """Get total market value of all positions."""
        return sum(pos.market_value for pos in self.positions.values())
    
    def get_total_value(self) -> float:
        """Get total portfolio value (cash + positions)."""
        return self.cash + self.get_positions_value()
    
    def get_total_return(self) -> float:
        """Get total return percentage."""
        total_value = self.get_total_value()
        return ((total_value - self.initial_capital) / self.initial_capital) * 100
    
    def get_trade_history_df(self) -> pd.DataFrame:
        """Get trade history as DataFrame."""
        if not self.trade_history:
            return pd.DataFrame()
        return pd.DataFrame(self.trade_history)
    
    def get_equity_curve_df(self) -> pd.DataFrame:
        """Get equity curve as DataFrame."""
        if not self.equity_curve:
            return pd.DataFrame()
        return pd.DataFrame(self.equity_curve)
    
    def get_positions_df(self) -> pd.DataFrame:
        """Get current positions as DataFrame."""
        if not self.positions:
            return pd.DataFrame()
        return pd.DataFrame([pos.to_dict() for pos in self.positions.values()])
    
    def get_summary(self) -> Dict:
        """Get portfolio summary statistics."""
        total_value = self.get_total_value()
        positions_value = self.get_positions_value()
        
        # Calculate returns
        total_return = self.get_total_return()
        
        # Win/loss stats from closed trades
        closed_trades = [t for t in self.trade_history if t['action'] == 'SELL']
        winning_trades = [t for t in closed_trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in closed_trades if t.get('pnl', 0) < 0]
        
        total_trades = len(closed_trades)
        win_rate = len(winning_trades) / total_trades * 100 if total_trades > 0 else 0
        
        avg_win = np.mean([t['pnl_pct'] for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t['pnl_pct'] for t in losing_trades]) if losing_trades else 0
        
        return {
            'initial_capital': self.initial_capital,
            'current_value': total_value,
            'cash': self.cash,
            'positions_value': positions_value,
            'total_return': total_return,
            'total_return_dollars': total_value - self.initial_capital,
            'num_positions': len(self.positions),
            'total_trades': len(self.trade_history),
            'closed_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'avg_win_pct': avg_win,
            'avg_loss_pct': avg_loss,
        }
    
    def print_summary(self):
        """Print portfolio summary."""
        summary = self.get_summary()
        
        print("=" * 80)
        print("PORTFOLIO SUMMARY")
        print("=" * 80)
        print(f"Initial Capital:     ${summary['initial_capital']:>15,.2f}")
        print(f"Current Value:       ${summary['current_value']:>15,.2f}")
        print(f"  Cash:              ${summary['cash']:>15,.2f}")
        print(f"  Positions:         ${summary['positions_value']:>15,.2f}")
        print(f"Total Return:        ${summary['total_return_dollars']:>15,.2f} ({summary['total_return']:>+6.2f}%)")
        print(f"\nCurrent Positions:   {summary['num_positions']:>15}")
        print(f"Total Trades:        {summary['total_trades']:>15}")
        print(f"Closed Trades:       {summary['closed_trades']:>15}")
        print(f"  Winners:           {summary['winning_trades']:>15}")
        print(f"  Losers:            {summary['losing_trades']:>15}")
        print(f"Win Rate:            {summary['win_rate']:>14.1f}%")
        if summary['avg_win_pct'] != 0:
            print(f"Avg Win:             {summary['avg_win_pct']:>14.2f}%")
        if summary['avg_loss_pct'] != 0:
            print(f"Avg Loss:            {summary['avg_loss_pct']:>14.2f}%")
        print("=" * 80)
