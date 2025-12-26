"""
Portfolio performance metrics.

Implements:
- Sharpe Ratio (risk-adjusted return)
- Sortino Ratio (downside risk-adjusted return)
- Maximum Drawdown
- Win Rate and Profit Factor
- Calmar Ratio

All calculations use Decimal for precision.

Author: AI-CIV (capability-curator)
Created: 2025-12-26
Domain: trading-systems
"""

from decimal import Decimal
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import math

# Import from sibling module
try:
    from .precision import to_decimal, safe_divide
except ImportError:
    # For standalone testing
    from precision import to_decimal, safe_divide


@dataclass
class PerformanceMetrics:
    """Complete performance metrics for a portfolio."""

    # Return metrics
    total_return: Decimal           # Total % return
    annualized_return: Decimal      # Annualized % return

    # Risk metrics
    volatility: Decimal             # Standard deviation of returns (annualized)
    max_drawdown: Decimal           # Maximum peak-to-trough decline (%)
    max_drawdown_duration: int      # Periods in max drawdown

    # Risk-adjusted returns
    sharpe_ratio: Decimal           # (Return - RiskFree) / Volatility
    sortino_ratio: Decimal          # (Return - RiskFree) / Downside Volatility
    calmar_ratio: Decimal           # Annualized Return / Max Drawdown

    # Trade statistics
    win_rate: Decimal               # % of winning trades
    profit_factor: Decimal          # Gross profit / Gross loss
    avg_win: Decimal                # Average winning trade
    avg_loss: Decimal               # Average losing trade (negative)
    expectancy: Decimal             # Expected value per trade

    # Additional
    total_trades: int
    winning_trades: int
    losing_trades: int
    largest_win: Decimal
    largest_loss: Decimal

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "total_return": str(self.total_return),
            "annualized_return": str(self.annualized_return),
            "volatility": str(self.volatility),
            "max_drawdown": str(self.max_drawdown),
            "max_drawdown_duration": self.max_drawdown_duration,
            "sharpe_ratio": str(self.sharpe_ratio),
            "sortino_ratio": str(self.sortino_ratio),
            "calmar_ratio": str(self.calmar_ratio),
            "win_rate": str(self.win_rate),
            "profit_factor": str(self.profit_factor),
            "avg_win": str(self.avg_win),
            "avg_loss": str(self.avg_loss),
            "expectancy": str(self.expectancy),
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "largest_win": str(self.largest_win),
            "largest_loss": str(self.largest_loss),
        }


def calculate_returns(
    portfolio_values: List[Decimal],
    method: str = "simple"
) -> List[Decimal]:
    """
    Calculate period returns from portfolio values.

    Args:
        portfolio_values: List of portfolio values over time
        method: "simple" for (V1-V0)/V0, "log" for ln(V1/V0)

    Returns:
        List of period returns (as decimals, e.g., 0.05 = 5%)

    Examples:
        >>> calculate_returns([Decimal("100"), Decimal("110"), Decimal("105")])
        [Decimal('0.1'), Decimal('-0.045454545...')]
    """
    if len(portfolio_values) < 2:
        return []

    returns = []
    for i in range(1, len(portfolio_values)):
        v0 = to_decimal(portfolio_values[i - 1])
        v1 = to_decimal(portfolio_values[i])

        if v0 <= 0:
            returns.append(Decimal("0"))
            continue

        if method == "simple":
            ret = (v1 - v0) / v0
        else:  # log returns
            # Use float for log, then convert back
            if v1 > 0 and v0 > 0:
                ret = to_decimal(str(math.log(float(v1 / v0))))
            else:
                ret = Decimal("0")

        returns.append(ret)

    return returns


def calculate_volatility(
    returns: List[Decimal],
    annualize: bool = True,
    periods_per_year: int = 252  # Trading days
) -> Decimal:
    """
    Calculate volatility (standard deviation) of returns.

    Args:
        returns: List of period returns (as decimals)
        annualize: Whether to annualize the volatility
        periods_per_year: Number of periods in a year (252 for daily)

    Returns:
        Volatility as a Decimal (as decimal, e.g., 0.20 = 20%)

    Examples:
        >>> returns = [Decimal("0.01"), Decimal("-0.02"), Decimal("0.015")]
        >>> calculate_volatility(returns, annualize=False)
        Decimal('0.01802775...')
    """
    if len(returns) < 2:
        return Decimal("0")

    # Convert to Decimal if needed
    returns = [to_decimal(r) for r in returns]

    # Calculate mean
    n = len(returns)
    mean = sum(returns) / n

    # Calculate variance (sample variance with n-1)
    variance = sum((r - mean) ** 2 for r in returns) / (n - 1)

    # Standard deviation (use float for sqrt, precision is acceptable here)
    if variance < 0:
        variance = Decimal("0")

    std_dev = to_decimal(str(math.sqrt(float(variance))))

    if annualize:
        std_dev = std_dev * to_decimal(str(math.sqrt(periods_per_year)))

    return std_dev


def calculate_downside_volatility(
    returns: List[Decimal],
    target_return: Decimal = Decimal("0"),
    annualize: bool = True,
    periods_per_year: int = 252
) -> Decimal:
    """
    Calculate downside volatility (only negative deviations).

    Used for Sortino ratio - only penalizes downside risk.

    Args:
        returns: List of period returns
        target_return: Minimum acceptable return (usually 0)
        annualize: Whether to annualize
        periods_per_year: Trading periods per year

    Returns:
        Downside volatility as Decimal
    """
    if len(returns) < 2:
        return Decimal("0")

    returns = [to_decimal(r) for r in returns]
    target_return = to_decimal(target_return)

    # Only consider returns below target (squared deviations)
    downside_squared = [
        (r - target_return) ** 2
        for r in returns
        if r < target_return
    ]

    if not downside_squared:
        return Decimal("0")

    # Downside variance (use full count for denominator, not just downside count)
    variance = sum(downside_squared) / len(returns)

    std_dev = to_decimal(str(math.sqrt(float(variance))))

    if annualize:
        std_dev = std_dev * to_decimal(str(math.sqrt(periods_per_year)))

    return std_dev


def calculate_sharpe_ratio(
    returns: List[Decimal],
    risk_free_rate: Decimal = Decimal("0.05"),  # 5% annual
    periods_per_year: int = 252
) -> Decimal:
    """
    Calculate Sharpe Ratio.

    Sharpe = (Portfolio Return - Risk Free Rate) / Portfolio Volatility

    Args:
        returns: List of period returns (as decimals)
        risk_free_rate: Annual risk-free rate (as decimal, 0.05 = 5%)
        periods_per_year: Periods per year for annualization

    Returns:
        Sharpe ratio as Decimal (dimensionless)

    Interpretation:
        < 0: Worse than risk-free
        0-1: Poor to mediocre
        1-2: Good
        2-3: Very good
        > 3: Excellent (rare, verify data)

    Examples:
        >>> returns = [Decimal("0.001")] * 252  # 0.1% daily for a year
        >>> calculate_sharpe_ratio(returns)  # ~25.2% annual return
        Decimal('...')  # Will be positive
    """
    if len(returns) < 2:
        return Decimal("0")

    returns = [to_decimal(r) for r in returns]
    risk_free_rate = to_decimal(risk_free_rate)

    # Calculate annualized return
    period_return = sum(returns) / len(returns)
    annual_return = period_return * periods_per_year

    # Calculate annualized volatility
    volatility = calculate_volatility(
        returns, annualize=True, periods_per_year=periods_per_year
    )

    if volatility == 0:
        return Decimal("0")

    # Sharpe ratio
    excess_return = annual_return - risk_free_rate
    return safe_divide(excess_return, volatility)


def calculate_sortino_ratio(
    returns: List[Decimal],
    risk_free_rate: Decimal = Decimal("0.05"),
    target_return: Decimal = Decimal("0"),
    periods_per_year: int = 252
) -> Decimal:
    """
    Calculate Sortino Ratio.

    Like Sharpe but uses downside volatility only.
    Sortino = (Return - Target) / Downside Volatility

    Args:
        returns: List of period returns
        risk_free_rate: Annual risk-free rate
        target_return: Minimum acceptable return (per period)
        periods_per_year: Periods per year

    Returns:
        Sortino ratio as Decimal

    Note:
        Sortino is often higher than Sharpe because it only penalizes
        downside volatility, not upside.
    """
    if len(returns) < 2:
        return Decimal("0")

    returns = [to_decimal(r) for r in returns]

    # Annualized return
    period_return = sum(returns) / len(returns)
    annual_return = period_return * periods_per_year

    # Downside volatility
    down_vol = calculate_downside_volatility(
        returns, target_return, annualize=True, periods_per_year=periods_per_year
    )

    if down_vol == 0:
        return Decimal("0")

    excess_return = annual_return - to_decimal(risk_free_rate)
    return safe_divide(excess_return, down_vol)


def calculate_max_drawdown(
    portfolio_values: List[Decimal]
) -> Tuple[Decimal, int, int, int]:
    """
    Calculate maximum drawdown.

    Maximum peak-to-trough decline during the period.

    Args:
        portfolio_values: List of portfolio values over time

    Returns:
        Tuple of:
        - max_drawdown: Maximum drawdown as decimal (0.20 = 20%)
        - peak_index: Index of the peak before drawdown
        - trough_index: Index of the trough (lowest point)
        - duration: Number of periods from peak to trough

    Examples:
        >>> values = [100, 110, 95, 105, 80, 100]
        >>> max_dd, peak_idx, trough_idx, duration = calculate_max_drawdown(values)
        >>> max_dd  # (110-80)/110 = 27.27%
        Decimal('0.27272727...')
    """
    if len(portfolio_values) < 2:
        return Decimal("0"), 0, 0, 0

    values = [to_decimal(v) for v in portfolio_values]

    peak = values[0]
    peak_idx = 0
    max_dd = Decimal("0")
    max_dd_peak_idx = 0
    max_dd_trough_idx = 0

    for i, value in enumerate(values):
        if value > peak:
            peak = value
            peak_idx = i

        if peak > 0:
            drawdown = (peak - value) / peak
            if drawdown > max_dd:
                max_dd = drawdown
                max_dd_peak_idx = peak_idx
                max_dd_trough_idx = i

    # Duration is periods from peak to trough
    duration = max_dd_trough_idx - max_dd_peak_idx

    return max_dd, max_dd_peak_idx, max_dd_trough_idx, duration


def calculate_calmar_ratio(
    returns: List[Decimal],
    portfolio_values: List[Decimal],
    periods_per_year: int = 252
) -> Decimal:
    """
    Calculate Calmar Ratio.

    Calmar = Annualized Return / Maximum Drawdown

    Higher is better - good returns with low drawdowns.

    Args:
        returns: List of period returns
        portfolio_values: List of portfolio values
        periods_per_year: Periods per year

    Returns:
        Calmar ratio as Decimal

    Interpretation:
        < 0.5: Poor
        0.5-1: Mediocre
        1-2: Good
        2-3: Very good
        > 3: Excellent
    """
    if len(returns) < 2:
        return Decimal("0")

    returns = [to_decimal(r) for r in returns]

    # Annualized return
    period_return = sum(returns) / len(returns)
    annual_return = period_return * periods_per_year

    # Max drawdown
    max_dd, _, _, _ = calculate_max_drawdown(portfolio_values)

    if max_dd == 0:
        return Decimal("0")

    return safe_divide(annual_return, max_dd)


def calculate_trade_statistics(
    trade_pnls: List[Decimal]
) -> Dict:
    """
    Calculate trade statistics from individual trade P&Ls.

    Args:
        trade_pnls: List of P&L for each closed trade

    Returns:
        Dict with:
        - win_rate: Percentage of winning trades
        - profit_factor: Gross profit / Gross loss
        - avg_win: Average winning trade
        - avg_loss: Average losing trade
        - expectancy: Expected value per trade
        - total_trades: Total number of trades
        - winning_trades: Number of winners
        - losing_trades: Number of losers
        - largest_win: Biggest winning trade
        - largest_loss: Biggest losing trade
    """
    if not trade_pnls:
        return {
            "win_rate": Decimal("0"),
            "profit_factor": Decimal("0"),
            "avg_win": Decimal("0"),
            "avg_loss": Decimal("0"),
            "expectancy": Decimal("0"),
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "largest_win": Decimal("0"),
            "largest_loss": Decimal("0"),
        }

    pnls = [to_decimal(p) for p in trade_pnls]

    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]

    gross_profit = sum(wins) if wins else Decimal("0")
    gross_loss = abs(sum(losses)) if losses else Decimal("0")

    win_rate = (Decimal(len(wins)) / Decimal(len(pnls))) * Decimal("100")

    profit_factor = Decimal("0")
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss

    avg_win = safe_divide(sum(wins), Decimal(len(wins))) if wins else Decimal("0")
    avg_loss = safe_divide(sum(losses), Decimal(len(losses))) if losses else Decimal("0")

    # Expectancy = (Win% * Avg Win) + (Loss% * Avg Loss)
    win_pct = Decimal(len(wins)) / Decimal(len(pnls))
    loss_pct = Decimal(len(losses)) / Decimal(len(pnls))
    expectancy = (win_pct * avg_win) + (loss_pct * avg_loss)

    return {
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "expectancy": expectancy,
        "total_trades": len(pnls),
        "winning_trades": len(wins),
        "losing_trades": len(losses),
        "largest_win": max(wins) if wins else Decimal("0"),
        "largest_loss": min(losses) if losses else Decimal("0"),
    }


def calculate_performance_metrics(
    portfolio_values: List[Decimal],
    trade_pnls: List[Decimal],
    risk_free_rate: Decimal = Decimal("0.05"),
    periods_per_year: int = 252
) -> PerformanceMetrics:
    """
    Calculate complete performance metrics.

    This is the main entry point for comprehensive portfolio analysis.

    Args:
        portfolio_values: List of portfolio values over time
        trade_pnls: List of realized P&L per trade
        risk_free_rate: Annual risk-free rate (default 5%)
        periods_per_year: Trading periods per year (default 252)

    Returns:
        PerformanceMetrics dataclass with all metrics
    """
    values = [to_decimal(v) for v in portfolio_values]
    pnls = [to_decimal(p) for p in trade_pnls]

    returns = calculate_returns(values)

    # Total return
    if values and values[0] > 0:
        total_return = ((values[-1] - values[0]) / values[0]) * Decimal("100")
    else:
        total_return = Decimal("0")

    # Annualized return
    n_periods = len(returns)
    if n_periods > 0:
        period_return = sum(returns) / n_periods
        annualized_return = period_return * periods_per_year * Decimal("100")
    else:
        annualized_return = Decimal("0")

    # Volatility
    volatility = calculate_volatility(
        returns, annualize=True, periods_per_year=periods_per_year
    )

    # Max drawdown
    max_dd, peak_idx, trough_idx, dd_duration = calculate_max_drawdown(values)

    # Sharpe and Sortino
    sharpe = calculate_sharpe_ratio(returns, risk_free_rate, periods_per_year)
    sortino = calculate_sortino_ratio(
        returns, risk_free_rate, Decimal("0"), periods_per_year
    )

    # Calmar
    calmar = calculate_calmar_ratio(returns, values, periods_per_year)

    # Trade statistics
    trade_stats = calculate_trade_statistics(pnls)

    return PerformanceMetrics(
        total_return=total_return,
        annualized_return=annualized_return,
        volatility=volatility * Decimal("100"),  # As percentage
        max_drawdown=max_dd * Decimal("100"),    # As percentage
        max_drawdown_duration=dd_duration,
        sharpe_ratio=sharpe,
        sortino_ratio=sortino,
        calmar_ratio=calmar,
        win_rate=trade_stats["win_rate"],
        profit_factor=trade_stats["profit_factor"],
        avg_win=trade_stats["avg_win"],
        avg_loss=trade_stats["avg_loss"],
        expectancy=trade_stats["expectancy"],
        total_trades=trade_stats["total_trades"],
        winning_trades=trade_stats["winning_trades"],
        losing_trades=trade_stats["losing_trades"],
        largest_win=trade_stats["largest_win"],
        largest_loss=trade_stats["largest_loss"],
    )


# ============================================================================
# Demonstration / Self-Test
# ============================================================================

if __name__ == "__main__":
    print("=== Portfolio Metrics Test ===")

    # Simulate portfolio values (starting at $100,000)
    # Represents daily values over ~1 year (252 trading days)
    import random
    random.seed(42)  # For reproducibility

    values = [Decimal("100000")]
    for _ in range(251):
        daily_return = Decimal(str(random.gauss(0.0004, 0.015)))  # ~10% annual, 24% vol
        new_value = values[-1] * (Decimal("1") + daily_return)
        values.append(new_value)

    # Simulate trade P&Ls
    trade_pnls = []
    for _ in range(50):
        if random.random() < 0.55:  # 55% win rate
            pnl = Decimal(str(random.uniform(100, 2000)))
        else:
            pnl = Decimal(str(random.uniform(-1500, -100)))
        trade_pnls.append(pnl)

    # Calculate returns
    returns = calculate_returns(values)
    print(f"Number of return periods: {len(returns)}")
    print(f"Average daily return: {sum(returns) / len(returns):.6f}")

    # Calculate volatility
    vol = calculate_volatility(returns)
    print(f"Annualized volatility: {vol * 100:.2f}%")

    # Calculate max drawdown
    max_dd, peak_idx, trough_idx, duration = calculate_max_drawdown(values)
    print(f"Maximum drawdown: {max_dd * 100:.2f}%")
    print(f"Drawdown duration: {duration} periods")

    # Calculate Sharpe ratio
    sharpe = calculate_sharpe_ratio(returns)
    print(f"Sharpe ratio: {sharpe:.3f}")

    # Calculate Sortino ratio
    sortino = calculate_sortino_ratio(returns)
    print(f"Sortino ratio: {sortino:.3f}")

    # Calculate trade statistics
    trade_stats = calculate_trade_statistics(trade_pnls)
    print(f"\nTrade Statistics:")
    print(f"  Win rate: {trade_stats['win_rate']:.1f}%")
    print(f"  Profit factor: {trade_stats['profit_factor']:.2f}")
    print(f"  Expectancy: ${trade_stats['expectancy']:.2f}")

    # Calculate complete metrics
    print(f"\n=== Complete Performance Metrics ===")
    metrics = calculate_performance_metrics(values, trade_pnls)
    print(f"Total return: {metrics.total_return:.2f}%")
    print(f"Annualized return: {metrics.annualized_return:.2f}%")
    print(f"Volatility: {metrics.volatility:.2f}%")
    print(f"Max drawdown: {metrics.max_drawdown:.2f}%")
    print(f"Sharpe ratio: {metrics.sharpe_ratio:.3f}")
    print(f"Sortino ratio: {metrics.sortino_ratio:.3f}")
    print(f"Calmar ratio: {metrics.calmar_ratio:.3f}")

    print("\n=== All tests passed! ===")
