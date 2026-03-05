"""
Performance metrics calculation module for NancyBot.

Calculates returns, risk metrics, and performance statistics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


def calculate_returns(equity_curve: pd.DataFrame) -> pd.Series:
    """
    Calculate daily returns from equity curve.
    
    Args:
        equity_curve: DataFrame with 'date' and 'total_value' columns
        
    Returns:
        Series of daily returns
    """
    returns = equity_curve['total_value'].pct_change()
    return returns.dropna()


def calculate_total_return(initial_capital: float, final_value: float) -> float:
    """
    Calculate total return percentage.
    
    Args:
        initial_capital: Starting capital
        final_value: Ending value
        
    Returns:
        Total return percentage
    """
    return ((final_value - initial_capital) / initial_capital) * 100


def calculate_annualized_return(total_return: float, days: int) -> float:
    """
    Calculate annualized return.
    
    Args:
        total_return: Total return as percentage
        days: Number of days in period
        
    Returns:
        Annualized return percentage
    """
    if days <= 0:
        return 0.0
    
    years = days / 365.25
    if years == 0:
        return 0.0
    
    return (((1 + total_return / 100) ** (1 / years)) - 1) * 100


def calculate_volatility(returns: pd.Series, annualize: bool = True) -> float:
    """
    Calculate volatility (standard deviation of returns).
    
    Args:
        returns: Series of returns
        annualize: Whether to annualize volatility
        
    Returns:
        Volatility percentage
    """
    if len(returns) < 2:
        return 0.0
    
    vol = returns.std()
    
    if annualize:
        vol = vol * np.sqrt(252)  # 252 trading days per year
    
    return vol * 100  # Convert to percentage


def calculate_sharpe_ratio(returns: pd.Series, 
                           risk_free_rate: float = 0.02,
                           annualize: bool = True) -> float:
    """
    Calculate Sharpe ratio.
    
    Args:
        returns: Series of returns
        risk_free_rate: Annual risk-free rate (default 2%)
        annualize: Whether to annualize the ratio
        
    Returns:
        Sharpe ratio
    """
    if len(returns) < 2:
        return 0.0
    
    # Calculate excess returns
    daily_rf = (1 + risk_free_rate) ** (1/252) - 1
    excess_returns = returns - daily_rf
    
    # Calculate Sharpe ratio
    mean_excess = excess_returns.mean()
    std_excess = excess_returns.std()
    
    if std_excess == 0:
        return 0.0
    
    sharpe = mean_excess / std_excess
    
    if annualize:
        sharpe = sharpe * np.sqrt(252)
    
    return sharpe


def calculate_max_drawdown(equity_curve: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate maximum drawdown.
    
    Args:
        equity_curve: DataFrame with 'date' and 'total_value' columns
        
    Returns:
        Dictionary with max_drawdown percentage and other drawdown metrics
    """
    if len(equity_curve) < 2:
        return {'max_drawdown': 0.0, 'max_drawdown_duration': 0}
    
    # Calculate running maximum
    cummax = equity_curve['total_value'].cummax()
    
    # Calculate drawdown
    drawdown = (equity_curve['total_value'] - cummax) / cummax * 100
    
    max_dd = drawdown.min()
    
    # Find drawdown duration (days in drawdown)
    in_drawdown = drawdown < 0
    if in_drawdown.any():
        # Find longest consecutive drawdown period
        drawdown_periods = []
        current_period = 0
        
        for is_dd in in_drawdown:
            if is_dd:
                current_period += 1
            else:
                if current_period > 0:
                    drawdown_periods.append(current_period)
                current_period = 0
        
        if current_period > 0:
            drawdown_periods.append(current_period)
        
        max_dd_duration = max(drawdown_periods) if drawdown_periods else 0
    else:
        max_dd_duration = 0
    
    return {
        'max_drawdown': max_dd,
        'max_drawdown_duration': max_dd_duration,
        'current_drawdown': drawdown.iloc[-1] if len(drawdown) > 0 else 0
    }


def calculate_win_rate(trade_history: pd.DataFrame) -> float:
    """
    Calculate win rate from trade history.
    
    Args:
        trade_history: DataFrame with trade history
        
    Returns:
        Win rate percentage
    """
    sells = trade_history[trade_history['action'] == 'SELL']
    
    if len(sells) == 0:
        return 0.0
    
    winners = (sells['pnl'] > 0).sum()
    return (winners / len(sells)) * 100


def calculate_profit_factor(trade_history: pd.DataFrame) -> float:
    """
    Calculate profit factor (gross profit / gross loss).
    
    Args:
        trade_history: DataFrame with trade history
        
    Returns:
        Profit factor
    """
    sells = trade_history[trade_history['action'] == 'SELL']
    
    if len(sells) == 0:
        return 0.0
    
    gross_profit = sells[sells['pnl'] > 0]['pnl'].sum()
    gross_loss = abs(sells[sells['pnl'] < 0]['pnl'].sum())
    
    if gross_loss == 0:
        return float('inf') if gross_profit > 0 else 0.0
    
    return gross_profit / gross_loss


def calculate_expectancy(trade_history: pd.DataFrame) -> float:
    """
    Calculate expectancy (average profit per trade).
    
    Args:
        trade_history: DataFrame with trade history
        
    Returns:
        Expectancy in dollars
    """
    sells = trade_history[trade_history['action'] == 'SELL']
    
    if len(sells) == 0:
        return 0.0
    
    return sells['pnl'].mean()


def calculate_comprehensive_metrics(portfolio_summary: Dict,
                                   equity_curve: pd.DataFrame,
                                   trade_history: pd.DataFrame,
                                   days: int,
                                   benchmark_returns: Optional[pd.Series] = None) -> Dict:
    """
    Calculate comprehensive performance metrics.
    
    Args:
        portfolio_summary: Portfolio summary dictionary
        equity_curve: Equity curve DataFrame
        trade_history: Trade history DataFrame
        days: Number of days in backtest
        benchmark_returns: Optional benchmark returns for comparison
        
    Returns:
        Dictionary of performance metrics
    """
    # Basic returns
    total_return = portfolio_summary['total_return']
    annualized_return = calculate_annualized_return(total_return, days)
    
    # Calculate returns series
    returns = calculate_returns(equity_curve)
    
    # Risk metrics
    volatility = calculate_volatility(returns, annualize=True)
    sharpe = calculate_sharpe_ratio(returns, annualize=True)
    
    # Drawdown
    dd_metrics = calculate_max_drawdown(equity_curve)
    
    # Trade metrics
    win_rate = calculate_win_rate(trade_history)
    profit_factor = calculate_profit_factor(trade_history)
    expectancy = calculate_expectancy(trade_history)
    
    metrics = {
        # Returns
        'total_return': total_return,
        'annualized_return': annualized_return,
        
        # Risk
        'volatility': volatility,
        'sharpe_ratio': sharpe,
        'max_drawdown': dd_metrics['max_drawdown'],
        'max_drawdown_duration': dd_metrics['max_drawdown_duration'],
        
        # Trading
        'total_trades': portfolio_summary['total_trades'],
        'closed_trades': portfolio_summary['closed_trades'],
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'expectancy': expectancy,
        'avg_win': portfolio_summary.get('avg_win_pct', 0),
        'avg_loss': portfolio_summary.get('avg_loss_pct', 0),
        
        # Capital
        'initial_capital': portfolio_summary['initial_capital'],
        'final_value': portfolio_summary['current_value'],
        'total_pnl': portfolio_summary['total_return_dollars'],
    }
    
    # Benchmark comparison
    if benchmark_returns is not None and len(benchmark_returns) > 0:
        bench_total_return = (benchmark_returns + 1).prod() - 1
        bench_annualized = calculate_annualized_return(bench_total_return * 100, days)
        bench_volatility = calculate_volatility(benchmark_returns, annualize=True)
        
        metrics['benchmark_return'] = bench_total_return * 100
        metrics['benchmark_annualized'] = bench_annualized
        metrics['benchmark_volatility'] = bench_volatility
        metrics['alpha'] = annualized_return - bench_annualized
        
        # Calculate beta if possible
        if len(returns) > 1 and len(benchmark_returns) > 1:
            # Align returns
            aligned_returns = pd.DataFrame({
                'strategy': returns,
                'benchmark': benchmark_returns
            }).dropna()
            
            if len(aligned_returns) > 1:
                covariance = aligned_returns['strategy'].cov(aligned_returns['benchmark'])
                benchmark_variance = aligned_returns['benchmark'].var()
                
                if benchmark_variance != 0:
                    metrics['beta'] = covariance / benchmark_variance
                else:
                    metrics['beta'] = 0.0
    
    return metrics


def print_metrics(metrics: Dict):
    """
    Print performance metrics in a formatted table.
    
    Args:
        metrics: Dictionary of performance metrics
    """
    print("=" * 80)
    print("PERFORMANCE METRICS")
    print("=" * 80)
    
    print("\n📊 RETURNS")
    print(f"  Total Return:           {metrics['total_return']:>10.2f}%")
    print(f"  Annualized Return:      {metrics['annualized_return']:>10.2f}%")
    
    if 'benchmark_return' in metrics:
        print(f"  Benchmark Return:       {metrics['benchmark_return']:>10.2f}%")
        print(f"  Benchmark Annualized:   {metrics['benchmark_annualized']:>10.2f}%")
        print(f"  Alpha:                  {metrics['alpha']:>10.2f}%")
    
    print("\n⚠️  RISK")
    print(f"  Volatility (Annual):    {metrics['volatility']:>10.2f}%")
    print(f"  Sharpe Ratio:           {metrics['sharpe_ratio']:>10.2f}")
    print(f"  Max Drawdown:           {metrics['max_drawdown']:>10.2f}%")
    print(f"  Max DD Duration:        {metrics['max_drawdown_duration']:>10.0f} days")
    
    if 'beta' in metrics:
        print(f"  Beta:                   {metrics['beta']:>10.2f}")
    
    print("\n💼 TRADING")
    print(f"  Total Trades:           {metrics['total_trades']:>10.0f}")
    print(f"  Closed Trades:          {metrics['closed_trades']:>10.0f}")
    print(f"  Win Rate:               {metrics['win_rate']:>10.1f}%")
    print(f"  Profit Factor:          {metrics['profit_factor']:>10.2f}")
    print(f"  Expectancy:             ${metrics['expectancy']:>9,.2f}")
    
    if metrics['avg_win'] != 0:
        print(f"  Average Win:            {metrics['avg_win']:>10.2f}%")
    if metrics['avg_loss'] != 0:
        print(f"  Average Loss:           {metrics['avg_loss']:>10.2f}%")
    
    print("\n💰 CAPITAL")
    print(f"  Initial Capital:        ${metrics['initial_capital']:>9,.2f}")
    print(f"  Final Value:            ${metrics['final_value']:>9,.2f}")
    print(f"  Total P&L:              ${metrics['total_pnl']:>9,.2f}")
    
    print("=" * 80)
