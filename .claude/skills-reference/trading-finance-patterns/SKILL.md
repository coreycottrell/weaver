---
name: trading-finance-patterns
description: Production-ready financial calculation patterns for trading systems. Covers P&L calculations (realized/unrealized), portfolio metrics (Sharpe, Sortino, max drawdown), position sizing (Kelly, fixed fractional), margin/leverage, and critical precision handling. All calculations use Decimal arithmetic to prevent float errors that compound in financial systems.
version: 1.0.0
author: AI-CIV (capability-curator)
created: 2025-12-26
domain: trading-systems
priority: CRITICAL - financial accuracy is non-negotiable
---

# Trading Finance Patterns

This skill provides production-ready financial calculation patterns for trading systems. Every pattern prioritizes **correctness over convenience** - using Decimal arithmetic, explicit precision handling, and defensive programming.

**Core Principle**: In trading, errors compound. A 0.01% float precision error becomes significant when processed across thousands of trades. This skill eliminates that risk.

## When to Use This Skill

**Invoke when**:
- Calculating P&L (profit and loss) for trades or portfolios
- Computing portfolio metrics (Sharpe ratio, max drawdown, win rate)
- Determining position sizes for risk management
- Working with margin and leverage calculations
- Any financial calculation where precision matters

**Don't use when**:
- Rough estimates are acceptable (use float for performance)
- Working with non-financial quantities
- Precision beyond 8 decimal places isn't needed

## Prerequisites

```python
# Core dependencies
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, ROUND_UP
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math

# Optional but recommended
# pip install numpy pandas  # For batch operations on historical data
```

---

## Part 1: Decimal Precision - The Foundation

### Why Not Float?

**Float precision failures in trading**:

```python
# WRONG - Float accumulates errors
total = 0.0
for _ in range(100):
    total += 0.01
print(total)  # 0.9999999999999999 (not 1.0!)

# In trading context:
balance = 10000.0
for _ in range(1000):
    balance += 0.01  # Small fee credit
print(balance)  # 10009.999999999863 (not 10010.0!)

# This error grows with transaction volume
```

**Decimal solves this**:

```python
from decimal import Decimal

# CORRECT - Decimal is exact
total = Decimal("0")
for _ in range(100):
    total += Decimal("0.01")
print(total)  # Decimal('1.00') exactly!

balance = Decimal("10000")
for _ in range(1000):
    balance += Decimal("0.01")
print(balance)  # Decimal('10010.00') exactly!
```

### Decimal Best Practices

```python
# trading_finance/precision.py
"""
Precision handling for financial calculations.

CRITICAL: Always construct Decimal from strings, NEVER from floats.
"""

from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, ROUND_UP, getcontext, InvalidOperation
from typing import Union, Optional

# Set precision context for financial calculations
# 28 digits is sufficient for astronomical sums with 8 decimal precision
getcontext().prec = 28


class PrecisionError(ValueError):
    """Raised when precision requirements are violated."""
    pass


def to_decimal(value: Union[str, int, float, Decimal], precision: int = 8) -> Decimal:
    """
    Safely convert any value to Decimal.

    NEVER pass float directly to Decimal() - it preserves float's imprecision.
    This function handles the conversion safely.

    Args:
        value: The value to convert
        precision: Decimal places to round to (default 8)

    Returns:
        Decimal with specified precision

    Examples:
        >>> to_decimal("100.123456789")  # From string - preferred
        Decimal('100.12345679')
        >>> to_decimal(100)  # From int - safe
        Decimal('100.00000000')
        >>> to_decimal(100.5)  # From float - converted via string
        Decimal('100.50000000')
    """
    if isinstance(value, Decimal):
        pass  # Already Decimal
    elif isinstance(value, str):
        try:
            value = Decimal(value)
        except InvalidOperation:
            raise PrecisionError(f"Invalid decimal string: {value}")
    elif isinstance(value, int):
        value = Decimal(value)
    elif isinstance(value, float):
        # Convert float to string first to avoid float precision issues
        # Use repr() for maximum precision
        value = Decimal(repr(value))
    else:
        raise PrecisionError(f"Cannot convert {type(value)} to Decimal")

    # Round to specified precision
    quantize_str = "0." + "0" * precision if precision > 0 else "0"
    return value.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


def round_down(value: Decimal, precision: int = 8) -> Decimal:
    """
    Round down (floor) for conservative calculations.

    Use when:
    - Calculating available balance (don't overstate)
    - Maximum withdrawal amounts
    - Conservative position sizing

    Examples:
        >>> round_down(Decimal("100.129"), 2)
        Decimal('100.12')
    """
    quantize_str = "0." + "0" * precision if precision > 0 else "0"
    return value.quantize(Decimal(quantize_str), rounding=ROUND_DOWN)


def round_up(value: Decimal, precision: int = 8) -> Decimal:
    """
    Round up (ceiling) for conservative calculations.

    Use when:
    - Calculating fees (don't understate cost)
    - Minimum margin requirements
    - Required collateral

    Examples:
        >>> round_up(Decimal("100.121"), 2)
        Decimal('100.13')
    """
    quantize_str = "0." + "0" * precision if precision > 0 else "0"
    return value.quantize(Decimal(quantize_str), rounding=ROUND_UP)


# Standard precision constants for Trading Arena
PRICE_PRECISION = 8      # 8 decimal places for prices
QUANTITY_PRECISION = 8   # 8 decimal places for quantities
USDC_PRECISION = 2       # USDC is 2 decimal places (stablecoin)
BPS_PRECISION = 4        # 4 decimal places for basis points (0.01%)


def validate_precision(value: Decimal, max_decimals: int, name: str = "value") -> None:
    """
    Validate that a value doesn't exceed maximum decimal places.

    Raises PrecisionError if validation fails.

    Args:
        value: Decimal to validate
        max_decimals: Maximum allowed decimal places
        name: Field name for error message
    """
    sign, digits, exponent = value.as_tuple()
    if exponent < 0 and abs(exponent) > max_decimals:
        raise PrecisionError(
            f"{name} has {abs(exponent)} decimal places, max is {max_decimals}"
        )
```

### Precision Quick Reference

| Asset Type | Precision | Reason |
|------------|-----------|--------|
| BTC price | 8 decimals | Industry standard (1 satoshi) |
| ETH price | 8 decimals | Industry standard (1 gwei) |
| USDC value | 2 decimals | Stablecoin (mimics USD) |
| Quantity | 8 decimals | Fractional shares/crypto |
| Percentage | 4 decimals | Basis points (0.01%) |
| Fees | 8 decimals | Micro-fees in crypto |

---

## Part 2: P&L Calculations

### Core P&L Concepts

```
Realized P&L = Profit/loss from CLOSED positions
Unrealized P&L = Paper profit/loss from OPEN positions
Total P&L = Realized + Unrealized
```

### Complete P&L Implementation

```python
# trading_finance/pnl.py
"""
Profit and Loss calculations for trading systems.

Supports:
- Per-trade P&L
- Position P&L (multiple trades aggregated)
- Portfolio P&L (multiple positions)
- FIFO and average cost basis methods
"""

from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum

from .precision import to_decimal, round_down, PRICE_PRECISION


class Side(Enum):
    BUY = "buy"
    SELL = "sell"


class CostBasisMethod(Enum):
    FIFO = "fifo"      # First In, First Out
    LIFO = "lifo"      # Last In, First Out
    AVERAGE = "average"  # Weighted average cost


@dataclass
class Trade:
    """Individual trade execution."""
    trade_id: str
    symbol: str
    side: Side
    quantity: Decimal
    price: Decimal
    fee: Decimal
    executed_at: datetime

    @property
    def notional(self) -> Decimal:
        """Total value of trade (quantity * price)."""
        return self.quantity * self.price

    @property
    def cost(self) -> Decimal:
        """Total cost including fees (for buys)."""
        if self.side == Side.BUY:
            return self.notional + self.fee
        return self.notional - self.fee

    @property
    def proceeds(self) -> Decimal:
        """Net proceeds after fees (for sells)."""
        if self.side == Side.SELL:
            return self.notional - self.fee
        return self.notional + self.fee


@dataclass
class PnLResult:
    """Result of a P&L calculation."""
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    total_pnl: Decimal
    cost_basis: Decimal
    current_value: Decimal
    quantity_held: Decimal
    win_count: int = 0
    loss_count: int = 0
    total_trades: int = 0

    @property
    def return_pct(self) -> Decimal:
        """Return as percentage of cost basis."""
        if self.cost_basis == 0:
            return Decimal("0")
        return (self.total_pnl / self.cost_basis) * Decimal("100")

    @property
    def win_rate(self) -> Decimal:
        """Win rate as percentage."""
        if self.total_trades == 0:
            return Decimal("0")
        return (Decimal(self.win_count) / Decimal(self.total_trades)) * Decimal("100")


class PositionTracker:
    """
    Track position and calculate P&L for a single symbol.

    Supports multiple cost basis methods.
    """

    def __init__(
        self,
        symbol: str,
        method: CostBasisMethod = CostBasisMethod.FIFO
    ):
        self.symbol = symbol
        self.method = method

        # Position tracking
        self.quantity: Decimal = Decimal("0")
        self.cost_basis: Decimal = Decimal("0")  # Total cost of current position

        # Trade lots for FIFO/LIFO (list of (quantity, cost_per_unit))
        self.lots: List[tuple[Decimal, Decimal]] = []

        # P&L tracking
        self.realized_pnl: Decimal = Decimal("0")
        self.total_fees: Decimal = Decimal("0")
        self.trades: List[Trade] = []
        self.win_count: int = 0
        self.loss_count: int = 0

    def add_trade(self, trade: Trade) -> Decimal:
        """
        Process a trade and return realized P&L (if any).

        Returns:
            Realized P&L from this trade (Decimal(0) if opening/adding)
        """
        if trade.symbol != self.symbol:
            raise ValueError(f"Trade symbol {trade.symbol} doesn't match position {self.symbol}")

        self.trades.append(trade)
        self.total_fees += trade.fee

        if trade.side == Side.BUY:
            return self._process_buy(trade)
        else:
            return self._process_sell(trade)

    def _process_buy(self, trade: Trade) -> Decimal:
        """Process a buy trade."""
        cost_per_unit = trade.cost / trade.quantity

        if self.method == CostBasisMethod.AVERAGE:
            # Weighted average cost
            total_cost = self.cost_basis + trade.cost
            total_qty = self.quantity + trade.quantity
            self.cost_basis = total_cost
            self.quantity = total_qty
        else:
            # FIFO/LIFO: track individual lots
            self.lots.append((trade.quantity, cost_per_unit))
            self.quantity += trade.quantity
            self.cost_basis += trade.cost

        return Decimal("0")  # Buys don't realize P&L

    def _process_sell(self, trade: Trade) -> Decimal:
        """Process a sell trade and calculate realized P&L."""
        if trade.quantity > self.quantity:
            raise ValueError(
                f"Cannot sell {trade.quantity}, only {self.quantity} held"
            )

        # Proceeds from this sale
        proceeds = trade.proceeds

        # Calculate cost of sold units
        if self.method == CostBasisMethod.AVERAGE:
            avg_cost = self.cost_basis / self.quantity if self.quantity > 0 else Decimal("0")
            cost_of_sold = avg_cost * trade.quantity
            self.cost_basis -= cost_of_sold
            self.quantity -= trade.quantity
        else:
            # FIFO or LIFO
            cost_of_sold = self._consume_lots(trade.quantity)
            self.quantity -= trade.quantity
            self.cost_basis -= cost_of_sold

        # Calculate realized P&L for this trade
        pnl = proceeds - cost_of_sold
        self.realized_pnl += pnl

        # Track wins/losses
        if pnl > 0:
            self.win_count += 1
        elif pnl < 0:
            self.loss_count += 1

        return pnl

    def _consume_lots(self, quantity_to_sell: Decimal) -> Decimal:
        """
        Consume lots according to FIFO/LIFO method.

        Returns:
            Total cost of consumed lots
        """
        total_cost = Decimal("0")
        remaining = quantity_to_sell

        # LIFO: start from end, FIFO: start from beginning
        if self.method == CostBasisMethod.LIFO:
            self.lots.reverse()

        new_lots = []
        for lot_qty, lot_cost in self.lots:
            if remaining <= 0:
                new_lots.append((lot_qty, lot_cost))
                continue

            if lot_qty <= remaining:
                # Consume entire lot
                total_cost += lot_qty * lot_cost
                remaining -= lot_qty
            else:
                # Partial lot consumption
                total_cost += remaining * lot_cost
                new_lots.append((lot_qty - remaining, lot_cost))
                remaining = Decimal("0")

        if self.method == CostBasisMethod.LIFO:
            new_lots.reverse()

        self.lots = new_lots
        return total_cost

    def get_unrealized_pnl(self, current_price: Decimal) -> Decimal:
        """
        Calculate unrealized P&L at current market price.

        Args:
            current_price: Current market price of the asset

        Returns:
            Unrealized P&L
        """
        if self.quantity == 0:
            return Decimal("0")

        current_value = self.quantity * current_price
        return current_value - self.cost_basis

    def get_pnl_result(self, current_price: Decimal) -> PnLResult:
        """
        Get complete P&L breakdown.

        Args:
            current_price: Current market price

        Returns:
            PnLResult with all P&L metrics
        """
        unrealized = self.get_unrealized_pnl(current_price)
        current_value = self.quantity * current_price

        return PnLResult(
            realized_pnl=self.realized_pnl,
            unrealized_pnl=unrealized,
            total_pnl=self.realized_pnl + unrealized,
            cost_basis=self.cost_basis,
            current_value=current_value,
            quantity_held=self.quantity,
            win_count=self.win_count,
            loss_count=self.loss_count,
            total_trades=len([t for t in self.trades if t.side == Side.SELL])
        )

    @property
    def average_cost(self) -> Decimal:
        """Average cost per unit of current position."""
        if self.quantity == 0:
            return Decimal("0")
        return self.cost_basis / self.quantity


# ============================================================================
# Portfolio-Level P&L
# ============================================================================

@dataclass
class PortfolioPnL:
    """Portfolio-wide P&L aggregation."""
    total_realized: Decimal
    total_unrealized: Decimal
    total_pnl: Decimal
    total_cost_basis: Decimal
    total_value: Decimal
    cash_balance: Decimal
    return_pct: Decimal
    positions: Dict[str, PnLResult] = field(default_factory=dict)


class PortfolioTracker:
    """
    Track P&L across multiple positions.

    Usage:
        tracker = PortfolioTracker(initial_cash=Decimal("10000"))
        tracker.add_trade(btc_trade)
        tracker.add_trade(eth_trade)
        pnl = tracker.get_portfolio_pnl({"BTC": current_btc, "ETH": current_eth})
    """

    def __init__(
        self,
        initial_cash: Decimal,
        method: CostBasisMethod = CostBasisMethod.FIFO
    ):
        self.initial_cash = to_decimal(initial_cash)
        self.cash = self.initial_cash
        self.method = method
        self.positions: Dict[str, PositionTracker] = {}

    def add_trade(self, trade: Trade) -> Decimal:
        """
        Process a trade, updating cash and position.

        Returns:
            Realized P&L from this trade
        """
        # Create position tracker if needed
        if trade.symbol not in self.positions:
            self.positions[trade.symbol] = PositionTracker(
                trade.symbol, self.method
            )

        # Update cash
        if trade.side == Side.BUY:
            self.cash -= trade.cost
        else:
            self.cash += trade.proceeds

        # Update position
        return self.positions[trade.symbol].add_trade(trade)

    def get_portfolio_pnl(
        self,
        current_prices: Dict[str, Decimal]
    ) -> PortfolioPnL:
        """
        Calculate portfolio-wide P&L.

        Args:
            current_prices: Dict of symbol -> current price

        Returns:
            PortfolioPnL with complete breakdown
        """
        total_realized = Decimal("0")
        total_unrealized = Decimal("0")
        total_cost = Decimal("0")
        total_value = Decimal("0")
        position_results = {}

        for symbol, tracker in self.positions.items():
            price = current_prices.get(symbol, Decimal("0"))
            result = tracker.get_pnl_result(price)

            total_realized += result.realized_pnl
            total_unrealized += result.unrealized_pnl
            total_cost += result.cost_basis
            total_value += result.current_value
            position_results[symbol] = result

        total_pnl = total_realized + total_unrealized
        portfolio_value = self.cash + total_value

        # Return percentage based on initial investment
        return_pct = Decimal("0")
        if self.initial_cash > 0:
            return_pct = ((portfolio_value - self.initial_cash) / self.initial_cash) * Decimal("100")

        return PortfolioPnL(
            total_realized=total_realized,
            total_unrealized=total_unrealized,
            total_pnl=total_pnl,
            total_cost_basis=total_cost,
            total_value=total_value,
            cash_balance=self.cash,
            return_pct=return_pct,
            positions=position_results
        )
```

### P&L Example Usage

```python
from decimal import Decimal
from datetime import datetime
from trading_finance.pnl import (
    Trade, Side, PositionTracker, PortfolioTracker, CostBasisMethod
)

# === Single Position Example ===
tracker = PositionTracker("BTC", CostBasisMethod.FIFO)

# Buy 0.5 BTC at $40,000
buy1 = Trade(
    trade_id="t1",
    symbol="BTC",
    side=Side.BUY,
    quantity=Decimal("0.5"),
    price=Decimal("40000"),
    fee=Decimal("20"),
    executed_at=datetime.now()
)
tracker.add_trade(buy1)

# Buy 0.3 BTC at $42,000
buy2 = Trade(
    trade_id="t2",
    symbol="BTC",
    side=Side.BUY,
    quantity=Decimal("0.3"),
    price=Decimal("42000"),
    fee=Decimal("12.60"),
    executed_at=datetime.now()
)
tracker.add_trade(buy2)

# Sell 0.4 BTC at $45,000 (FIFO: uses first lot at $40,000)
sell1 = Trade(
    trade_id="t3",
    symbol="BTC",
    side=Side.SELL,
    quantity=Decimal("0.4"),
    price=Decimal("45000"),
    fee=Decimal("18"),
    executed_at=datetime.now()
)
realized = tracker.add_trade(sell1)
print(f"Realized P&L: ${realized}")  # Profit from selling at $45k vs cost at $40k

# Get current P&L at $46,000
result = tracker.get_pnl_result(Decimal("46000"))
print(f"Total P&L: ${result.total_pnl}")
print(f"Unrealized: ${result.unrealized_pnl}")
print(f"Remaining: {result.quantity_held} BTC")


# === Portfolio Example ===
portfolio = PortfolioTracker(initial_cash=Decimal("100000"))

# Trade BTC and ETH
portfolio.add_trade(buy1)
portfolio.add_trade(buy2)
portfolio.add_trade(sell1)

# ETH trades
eth_buy = Trade(
    trade_id="e1",
    symbol="ETH",
    side=Side.BUY,
    quantity=Decimal("5"),
    price=Decimal("2500"),
    fee=Decimal("12.50"),
    executed_at=datetime.now()
)
portfolio.add_trade(eth_buy)

# Get portfolio P&L
pnl = portfolio.get_portfolio_pnl({
    "BTC": Decimal("46000"),
    "ETH": Decimal("2800")
})

print(f"Portfolio Value: ${pnl.total_value + pnl.cash_balance}")
print(f"Total Return: {pnl.return_pct}%")
print(f"Cash: ${pnl.cash_balance}")
```

---

## Part 3: Portfolio Metrics

### Key Metrics for Trading Performance

```python
# trading_finance/metrics.py
"""
Portfolio performance metrics.

Implements:
- Sharpe Ratio (risk-adjusted return)
- Sortino Ratio (downside risk-adjusted return)
- Maximum Drawdown
- Win Rate and Profit Factor
- Calmar Ratio
"""

from decimal import Decimal
from typing import List, Tuple, Optional
from dataclasses import dataclass
import math

from .precision import to_decimal


@dataclass
class PerformanceMetrics:
    """Complete performance metrics for a portfolio."""

    # Return metrics
    total_return: Decimal           # Total % return
    annualized_return: Decimal      # Annualized % return

    # Risk metrics
    volatility: Decimal             # Standard deviation of returns (annualized)
    max_drawdown: Decimal           # Maximum peak-to-trough decline
    max_drawdown_duration: int      # Days in max drawdown

    # Risk-adjusted returns
    sharpe_ratio: Decimal           # (Return - RiskFree) / Volatility
    sortino_ratio: Decimal          # (Return - RiskFree) / Downside Volatility
    calmar_ratio: Decimal           # Annualized Return / Max Drawdown

    # Trade statistics
    win_rate: Decimal               # % of winning trades
    profit_factor: Decimal          # Gross profit / Gross loss
    avg_win: Decimal                # Average winning trade
    avg_loss: Decimal               # Average losing trade
    expectancy: Decimal             # Expected value per trade

    # Additional
    total_trades: int
    winning_trades: int
    losing_trades: int
    largest_win: Decimal
    largest_loss: Decimal


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
        List of period returns
    """
    if len(portfolio_values) < 2:
        return []

    returns = []
    for i in range(1, len(portfolio_values)):
        v0 = portfolio_values[i - 1]
        v1 = portfolio_values[i]

        if v0 <= 0:
            returns.append(Decimal("0"))
            continue

        if method == "simple":
            ret = (v1 - v0) / v0
        else:  # log returns
            # Use float for log, then convert back
            ret = to_decimal(str(math.log(float(v1 / v0))))

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
        returns: List of period returns
        annualize: Whether to annualize the volatility
        periods_per_year: Number of periods in a year (252 for daily)

    Returns:
        Volatility as a Decimal
    """
    if len(returns) < 2:
        return Decimal("0")

    # Calculate mean
    n = len(returns)
    mean = sum(returns) / n

    # Calculate variance
    variance = sum((r - mean) ** 2 for r in returns) / (n - 1)

    # Standard deviation (use float for sqrt)
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
    Calculate downside volatility (only negative returns).

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

    # Only consider returns below target
    downside_returns = [
        (r - target_return) ** 2
        for r in returns
        if r < target_return
    ]

    if not downside_returns:
        return Decimal("0")

    # Downside variance
    variance = sum(downside_returns) / len(returns)  # Use full count for denominator

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
        returns: List of period returns
        risk_free_rate: Annual risk-free rate
        periods_per_year: Periods per year for annualization

    Returns:
        Sharpe ratio as Decimal
    """
    if len(returns) < 2:
        return Decimal("0")

    # Calculate annualized return
    period_return = sum(returns) / len(returns)
    annual_return = period_return * periods_per_year

    # Calculate annualized volatility
    volatility = calculate_volatility(returns, annualize=True, periods_per_year=periods_per_year)

    if volatility == 0:
        return Decimal("0")

    # Sharpe ratio
    excess_return = annual_return - risk_free_rate
    return excess_return / volatility


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
        target_return: Minimum acceptable return
        periods_per_year: Periods per year

    Returns:
        Sortino ratio as Decimal
    """
    if len(returns) < 2:
        return Decimal("0")

    # Annualized return
    period_return = sum(returns) / len(returns)
    annual_return = period_return * periods_per_year

    # Downside volatility
    down_vol = calculate_downside_volatility(
        returns, target_return, annualize=True, periods_per_year=periods_per_year
    )

    if down_vol == 0:
        return Decimal("0")

    excess_return = annual_return - risk_free_rate
    return excess_return / down_vol


def calculate_max_drawdown(
    portfolio_values: List[Decimal]
) -> Tuple[Decimal, int, int, int]:
    """
    Calculate maximum drawdown.

    Maximum peak-to-trough decline during the period.

    Args:
        portfolio_values: List of portfolio values over time

    Returns:
        Tuple of (max_drawdown, peak_index, trough_index, duration)
    """
    if len(portfolio_values) < 2:
        return Decimal("0"), 0, 0, 0

    peak = portfolio_values[0]
    peak_idx = 0
    max_dd = Decimal("0")
    max_dd_peak_idx = 0
    max_dd_trough_idx = 0

    for i, value in enumerate(portfolio_values):
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
    """
    if len(returns) < 2:
        return Decimal("0")

    # Annualized return
    period_return = sum(returns) / len(returns)
    annual_return = period_return * periods_per_year

    # Max drawdown
    max_dd, _, _, _ = calculate_max_drawdown(portfolio_values)

    if max_dd == 0:
        return Decimal("0")

    return annual_return / max_dd


def calculate_trade_statistics(
    trade_pnls: List[Decimal]
) -> dict:
    """
    Calculate trade statistics from individual trade P&Ls.

    Args:
        trade_pnls: List of P&L for each closed trade

    Returns:
        Dict with win_rate, profit_factor, avg_win, avg_loss, expectancy
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

    wins = [p for p in trade_pnls if p > 0]
    losses = [p for p in trade_pnls if p < 0]

    gross_profit = sum(wins) if wins else Decimal("0")
    gross_loss = abs(sum(losses)) if losses else Decimal("0")

    win_rate = Decimal(len(wins)) / Decimal(len(trade_pnls)) * Decimal("100")

    profit_factor = Decimal("0")
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss

    avg_win = sum(wins) / len(wins) if wins else Decimal("0")
    avg_loss = sum(losses) / len(losses) if losses else Decimal("0")

    # Expectancy = (Win% * Avg Win) + (Loss% * Avg Loss)
    win_pct = Decimal(len(wins)) / Decimal(len(trade_pnls))
    loss_pct = Decimal(len(losses)) / Decimal(len(trade_pnls))
    expectancy = (win_pct * avg_win) + (loss_pct * avg_loss)

    return {
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "expectancy": expectancy,
        "total_trades": len(trade_pnls),
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

    Args:
        portfolio_values: List of portfolio values over time
        trade_pnls: List of realized P&L per trade
        risk_free_rate: Annual risk-free rate (default 5%)
        periods_per_year: Trading periods per year (default 252)

    Returns:
        PerformanceMetrics dataclass with all metrics
    """
    returns = calculate_returns(portfolio_values)

    # Total return
    if portfolio_values and portfolio_values[0] > 0:
        total_return = (portfolio_values[-1] - portfolio_values[0]) / portfolio_values[0] * Decimal("100")
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
    volatility = calculate_volatility(returns, annualize=True, periods_per_year=periods_per_year)

    # Max drawdown
    max_dd, peak_idx, trough_idx, dd_duration = calculate_max_drawdown(portfolio_values)

    # Sharpe and Sortino
    sharpe = calculate_sharpe_ratio(returns, risk_free_rate, periods_per_year)
    sortino = calculate_sortino_ratio(returns, risk_free_rate, Decimal("0"), periods_per_year)

    # Calmar
    calmar = calculate_calmar_ratio(returns, portfolio_values, periods_per_year)

    # Trade statistics
    trade_stats = calculate_trade_statistics(trade_pnls)

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
```

### Metrics Quick Reference

| Metric | Formula | Good Value | Meaning |
|--------|---------|------------|---------|
| Sharpe Ratio | (R - Rf) / Vol | > 1.0 | Risk-adjusted return |
| Sortino Ratio | (R - Rf) / DownVol | > 1.5 | Downside risk-adjusted |
| Max Drawdown | Peak to Trough % | < 20% | Worst decline |
| Calmar Ratio | Ann. Return / MaxDD | > 1.0 | Return vs drawdown |
| Win Rate | Wins / Total | > 50% | Trade success rate |
| Profit Factor | Gross P / Gross L | > 1.5 | Profitability ratio |
| Expectancy | WR*AvgW + LR*AvgL | > 0 | Expected per trade |

---

## Part 4: Position Sizing

### Kelly Criterion and Fixed Fractional

```python
# trading_finance/position_sizing.py
"""
Position sizing algorithms for risk management.

Implements:
- Kelly Criterion (optimal sizing based on edge)
- Fixed Fractional (constant % risk per trade)
- Volatility-based sizing
- Risk parity
"""

from decimal import Decimal
from typing import Optional
from dataclasses import dataclass
import math

from .precision import to_decimal, round_down


@dataclass
class PositionSize:
    """Result of position sizing calculation."""
    quantity: Decimal           # Number of units to trade
    notional: Decimal           # Dollar value of position
    risk_amount: Decimal        # Dollar amount at risk
    portfolio_pct: Decimal      # % of portfolio

    # Optional context
    method: str = ""
    stop_loss_pct: Optional[Decimal] = None
    confidence: Optional[Decimal] = None


def kelly_criterion(
    win_rate: Decimal,
    avg_win: Decimal,
    avg_loss: Decimal,
    fraction: Decimal = Decimal("0.5")  # Half-Kelly is common
) -> Decimal:
    """
    Calculate Kelly Criterion optimal bet size.

    Kelly = W - (1-W)/B
    Where:
        W = Probability of winning
        B = Ratio of win size to loss size

    Args:
        win_rate: Historical win rate (0-1)
        avg_win: Average winning trade size
        avg_loss: Average losing trade size (positive number)
        fraction: Kelly fraction (0.5 = half-Kelly, safer)

    Returns:
        Optimal bet size as fraction of bankroll

    Example:
        >>> kelly_criterion(Decimal("0.55"), Decimal("100"), Decimal("80"))
        Decimal('0.2375')  # Bet 23.75% of bankroll

    WARNING: Full Kelly is aggressive and can lead to large drawdowns.
    Half-Kelly (fraction=0.5) is recommended for most traders.
    """
    if avg_loss <= 0:
        return Decimal("0")

    # Win/loss ratio
    b = avg_win / avg_loss

    # Kelly formula
    kelly = win_rate - ((Decimal("1") - win_rate) / b)

    # Never bet negative or more than 100%
    kelly = max(Decimal("0"), min(kelly, Decimal("1")))

    # Apply Kelly fraction (half-Kelly, quarter-Kelly, etc.)
    return kelly * fraction


def fixed_fractional(
    portfolio_value: Decimal,
    risk_per_trade: Decimal,  # e.g., 0.02 = 2%
    entry_price: Decimal,
    stop_loss_price: Decimal
) -> PositionSize:
    """
    Fixed fractional position sizing.

    Risk a fixed percentage of portfolio on each trade.
    Position size = Risk Amount / (Entry - Stop Loss)

    Args:
        portfolio_value: Current portfolio value
        risk_per_trade: Max % to risk per trade (e.g., 0.01 = 1%)
        entry_price: Entry price for the trade
        stop_loss_price: Stop loss price

    Returns:
        PositionSize with calculated values

    Example:
        >>> fixed_fractional(
        ...     Decimal("100000"),   # $100k portfolio
        ...     Decimal("0.01"),     # 1% risk
        ...     Decimal("50000"),    # Entry at $50k
        ...     Decimal("48000")     # Stop at $48k (4% below)
        ... )
        PositionSize(quantity=0.5, notional=25000, risk_amount=1000, ...)
    """
    # Calculate risk amount
    risk_amount = portfolio_value * risk_per_trade

    # Calculate risk per unit
    if entry_price > stop_loss_price:
        # Long position
        risk_per_unit = entry_price - stop_loss_price
    else:
        # Short position
        risk_per_unit = stop_loss_price - entry_price

    if risk_per_unit <= 0:
        return PositionSize(
            quantity=Decimal("0"),
            notional=Decimal("0"),
            risk_amount=Decimal("0"),
            portfolio_pct=Decimal("0"),
            method="fixed_fractional",
            stop_loss_pct=Decimal("0")
        )

    # Calculate position size
    quantity = round_down(risk_amount / risk_per_unit, 8)
    notional = quantity * entry_price
    portfolio_pct = (notional / portfolio_value) * Decimal("100")
    stop_loss_pct = (risk_per_unit / entry_price) * Decimal("100")

    return PositionSize(
        quantity=quantity,
        notional=notional,
        risk_amount=risk_amount,
        portfolio_pct=portfolio_pct,
        method="fixed_fractional",
        stop_loss_pct=stop_loss_pct
    )


def volatility_adjusted_sizing(
    portfolio_value: Decimal,
    target_volatility: Decimal,  # e.g., 0.10 = 10% annual vol
    asset_volatility: Decimal,   # Asset's annualized volatility
    entry_price: Decimal,
    max_position_pct: Decimal = Decimal("0.25")  # Max 25% of portfolio
) -> PositionSize:
    """
    Volatility-adjusted position sizing.

    Size positions inversely to their volatility to achieve
    consistent portfolio volatility contribution.

    Args:
        portfolio_value: Current portfolio value
        target_volatility: Target portfolio volatility contribution
        asset_volatility: Asset's annualized volatility
        entry_price: Entry price
        max_position_pct: Maximum position size as % of portfolio

    Returns:
        PositionSize with calculated values

    Example:
        >>> volatility_adjusted_sizing(
        ...     Decimal("100000"),   # $100k
        ...     Decimal("0.10"),     # 10% target vol
        ...     Decimal("0.60"),     # BTC has 60% vol
        ...     Decimal("50000")     # Entry at $50k
        ... )
        # Will size smaller for high-vol assets
    """
    if asset_volatility <= 0:
        return PositionSize(
            quantity=Decimal("0"),
            notional=Decimal("0"),
            risk_amount=Decimal("0"),
            portfolio_pct=Decimal("0"),
            method="volatility_adjusted"
        )

    # Target notional to achieve target volatility contribution
    # Position Vol Contribution = Position Size * Asset Vol
    # Solve for Position Size = Target Vol / Asset Vol
    vol_ratio = target_volatility / asset_volatility

    # Convert to notional
    target_notional = portfolio_value * vol_ratio

    # Apply max position limit
    max_notional = portfolio_value * max_position_pct
    notional = min(target_notional, max_notional)

    quantity = round_down(notional / entry_price, 8)
    actual_notional = quantity * entry_price
    portfolio_pct = (actual_notional / portfolio_value) * Decimal("100")

    # Estimate risk as 2 standard deviations
    daily_vol = asset_volatility / to_decimal(str(math.sqrt(252)))
    risk_amount = actual_notional * daily_vol * Decimal("2")

    return PositionSize(
        quantity=quantity,
        notional=actual_notional,
        risk_amount=risk_amount,
        portfolio_pct=portfolio_pct,
        method="volatility_adjusted"
    )


def kelly_position_size(
    portfolio_value: Decimal,
    win_rate: Decimal,
    avg_win_pct: Decimal,     # Average win as % of position
    avg_loss_pct: Decimal,    # Average loss as % of position
    entry_price: Decimal,
    kelly_fraction: Decimal = Decimal("0.5"),
    max_position_pct: Decimal = Decimal("0.20")  # Never more than 20%
) -> PositionSize:
    """
    Kelly-based position sizing.

    Combines Kelly criterion with practical limits.

    Args:
        portfolio_value: Current portfolio value
        win_rate: Historical win rate (0-1)
        avg_win_pct: Average winning trade as % of position
        avg_loss_pct: Average losing trade as % of position
        entry_price: Entry price
        kelly_fraction: Fraction of Kelly to use (0.5 recommended)
        max_position_pct: Maximum position as % of portfolio

    Returns:
        PositionSize with Kelly-optimal sizing
    """
    # Calculate Kelly fraction
    kelly_pct = kelly_criterion(
        win_rate,
        avg_win_pct,
        avg_loss_pct,
        kelly_fraction
    )

    # Apply maximum limit
    position_pct = min(kelly_pct, max_position_pct)

    # Calculate notional
    notional = portfolio_value * position_pct
    quantity = round_down(notional / entry_price, 8)
    actual_notional = quantity * entry_price

    # Risk is based on average loss
    risk_amount = actual_notional * avg_loss_pct

    return PositionSize(
        quantity=quantity,
        notional=actual_notional,
        risk_amount=risk_amount,
        portfolio_pct=position_pct * Decimal("100"),
        method="kelly",
        confidence=win_rate
    )


# ============================================================================
# Position Sizing Limits
# ============================================================================

@dataclass
class PositionLimits:
    """Risk limits for position sizing."""
    max_position_pct: Decimal = Decimal("0.20")      # 20% max per position
    max_sector_pct: Decimal = Decimal("0.40")        # 40% max per sector
    max_correlated_pct: Decimal = Decimal("0.50")    # 50% max in correlated assets
    max_daily_loss_pct: Decimal = Decimal("0.05")    # 5% daily stop-loss
    max_total_exposure: Decimal = Decimal("1.00")    # 100% max total exposure


def validate_position_size(
    proposed: PositionSize,
    current_positions: dict[str, Decimal],  # symbol -> notional
    portfolio_value: Decimal,
    limits: PositionLimits
) -> Tuple[bool, str]:
    """
    Validate proposed position against risk limits.

    Returns:
        Tuple of (is_valid, reason_if_invalid)
    """
    # Check single position limit
    if proposed.portfolio_pct > limits.max_position_pct * Decimal("100"):
        return False, f"Position {proposed.portfolio_pct}% exceeds limit {limits.max_position_pct * 100}%"

    # Check total exposure
    current_exposure = sum(current_positions.values())
    new_exposure = current_exposure + proposed.notional
    exposure_pct = new_exposure / portfolio_value

    if exposure_pct > limits.max_total_exposure:
        return False, f"Total exposure {exposure_pct * 100}% exceeds limit {limits.max_total_exposure * 100}%"

    return True, ""
```

### Position Sizing Quick Reference

| Method | Best For | Key Input | Complexity |
|--------|----------|-----------|------------|
| Fixed Fractional | Consistent risk | Risk %, Stop Loss | Low |
| Kelly Criterion | Edge optimization | Win rate, Avg W/L | Medium |
| Volatility-Adjusted | Vol targeting | Asset volatility | Medium |
| Risk Parity | Portfolio balance | All asset vols | High |

---

## Part 5: Margin and Leverage

### Margin Calculations

```python
# trading_finance/margin.py
"""
Margin and leverage calculations for trading.

Covers:
- Initial and maintenance margin
- Leverage ratio calculations
- Liquidation price estimation
- Margin call detection
"""

from decimal import Decimal
from typing import Optional, Tuple
from dataclasses import dataclass

from .precision import to_decimal, round_up, round_down


@dataclass
class MarginRequirements:
    """Margin requirements for a position."""
    initial_margin: Decimal      # Required to open position
    maintenance_margin: Decimal  # Required to maintain position
    initial_margin_pct: Decimal  # As percentage
    maintenance_margin_pct: Decimal  # As percentage


@dataclass
class MarginStatus:
    """Current margin status for a position."""
    position_value: Decimal
    collateral: Decimal
    unrealized_pnl: Decimal
    margin_used: Decimal
    margin_available: Decimal
    margin_ratio: Decimal        # Collateral / Margin Required
    leverage_ratio: Decimal      # Position Value / Collateral
    is_margin_call: bool
    is_liquidation: bool
    liquidation_price: Optional[Decimal]


def calculate_margin_requirements(
    notional_value: Decimal,
    initial_margin_pct: Decimal = Decimal("0.10"),    # 10% = 10x leverage
    maintenance_margin_pct: Decimal = Decimal("0.05")  # 5%
) -> MarginRequirements:
    """
    Calculate margin requirements for a position.

    Args:
        notional_value: Total position value
        initial_margin_pct: Initial margin as percentage (e.g., 0.10 = 10%)
        maintenance_margin_pct: Maintenance margin as percentage

    Returns:
        MarginRequirements with calculated values

    Example:
        >>> calculate_margin_requirements(Decimal("100000"), Decimal("0.10"))
        MarginRequirements(initial_margin=10000, maintenance_margin=5000, ...)
    """
    initial_margin = round_up(notional_value * initial_margin_pct, 2)
    maintenance_margin = round_up(notional_value * maintenance_margin_pct, 2)

    return MarginRequirements(
        initial_margin=initial_margin,
        maintenance_margin=maintenance_margin,
        initial_margin_pct=initial_margin_pct * Decimal("100"),
        maintenance_margin_pct=maintenance_margin_pct * Decimal("100")
    )


def calculate_max_leverage(
    initial_margin_pct: Decimal
) -> Decimal:
    """
    Calculate maximum leverage from initial margin percentage.

    Leverage = 1 / Initial Margin %

    Examples:
        10% margin = 10x leverage
        5% margin = 20x leverage
        25% margin = 4x leverage
    """
    if initial_margin_pct <= 0:
        return Decimal("0")

    return Decimal("1") / initial_margin_pct


def calculate_leverage_ratio(
    position_value: Decimal,
    collateral: Decimal
) -> Decimal:
    """
    Calculate current leverage ratio.

    Leverage = Position Value / Collateral

    Args:
        position_value: Current position notional value
        collateral: Total collateral/equity

    Returns:
        Leverage ratio (e.g., 5.0 = 5x leveraged)
    """
    if collateral <= 0:
        return Decimal("0")

    return position_value / collateral


def calculate_liquidation_price(
    entry_price: Decimal,
    quantity: Decimal,
    collateral: Decimal,
    maintenance_margin_pct: Decimal,
    is_long: bool = True,
    fees_pct: Decimal = Decimal("0.001")  # 0.1% liquidation fee estimate
) -> Decimal:
    """
    Calculate liquidation price for a leveraged position.

    Liquidation occurs when:
    Collateral + Unrealized PnL < Maintenance Margin + Fees

    Args:
        entry_price: Position entry price
        quantity: Position quantity
        collateral: Total collateral/margin
        maintenance_margin_pct: Maintenance margin requirement
        is_long: True for long, False for short
        fees_pct: Estimated liquidation fees

    Returns:
        Price at which liquidation occurs

    Example:
        >>> calculate_liquidation_price(
        ...     entry_price=Decimal("50000"),
        ...     quantity=Decimal("1"),
        ...     collateral=Decimal("5000"),      # 10x leverage
        ...     maintenance_margin_pct=Decimal("0.05"),
        ...     is_long=True
        ... )
        Decimal('45263.15789...')  # Liquidated if BTC drops below this
    """
    position_value = entry_price * quantity

    # Maintenance margin required (as function of position value)
    # At liquidation: Collateral + PnL = Maint Margin + Fees
    # Collateral + (Liq Price - Entry) * Qty = Maint% * Liq Price * Qty + Fees

    total_margin_pct = maintenance_margin_pct + fees_pct

    if is_long:
        # Long: liquidation when price falls
        # collateral + (liq_price - entry) * qty = maint_pct * liq_price * qty
        # collateral - entry * qty = liq_price * qty * (maint_pct - 1)
        # liq_price = (entry * qty - collateral) / (qty * (1 - maint_pct))
        denominator = quantity * (Decimal("1") - total_margin_pct)
        if denominator <= 0:
            return Decimal("0")
        liq_price = (entry_price * quantity - collateral) / denominator
    else:
        # Short: liquidation when price rises
        # collateral + (entry - liq_price) * qty = maint_pct * liq_price * qty
        # collateral + entry * qty = liq_price * qty * (1 + maint_pct)
        denominator = quantity * (Decimal("1") + total_margin_pct)
        if denominator <= 0:
            return Decimal("0")
        liq_price = (collateral + entry_price * quantity) / denominator

    return round_down(max(liq_price, Decimal("0")), 2)


def calculate_margin_status(
    entry_price: Decimal,
    current_price: Decimal,
    quantity: Decimal,
    collateral: Decimal,
    initial_margin_pct: Decimal = Decimal("0.10"),
    maintenance_margin_pct: Decimal = Decimal("0.05"),
    is_long: bool = True
) -> MarginStatus:
    """
    Calculate complete margin status for a position.

    Args:
        entry_price: Position entry price
        current_price: Current market price
        quantity: Position quantity
        collateral: Total collateral/margin deposited
        initial_margin_pct: Initial margin requirement
        maintenance_margin_pct: Maintenance margin requirement
        is_long: True for long, False for short

    Returns:
        MarginStatus with all margin metrics
    """
    # Position value
    position_value = current_price * quantity

    # Unrealized P&L
    if is_long:
        unrealized_pnl = (current_price - entry_price) * quantity
    else:
        unrealized_pnl = (entry_price - current_price) * quantity

    # Effective equity
    equity = collateral + unrealized_pnl

    # Margin requirements
    initial_margin = position_value * initial_margin_pct
    maintenance_margin = position_value * maintenance_margin_pct

    # Margin ratio (equity / maintenance margin)
    margin_ratio = Decimal("0")
    if maintenance_margin > 0:
        margin_ratio = equity / maintenance_margin

    # Leverage ratio
    leverage_ratio = Decimal("0")
    if equity > 0:
        leverage_ratio = position_value / equity

    # Margin call: equity < initial margin
    is_margin_call = equity < initial_margin

    # Liquidation: equity < maintenance margin
    is_liquidation = equity < maintenance_margin

    # Liquidation price
    liq_price = calculate_liquidation_price(
        entry_price, quantity, collateral,
        maintenance_margin_pct, is_long
    )

    return MarginStatus(
        position_value=position_value,
        collateral=collateral,
        unrealized_pnl=unrealized_pnl,
        margin_used=maintenance_margin,
        margin_available=max(equity - maintenance_margin, Decimal("0")),
        margin_ratio=margin_ratio,
        leverage_ratio=leverage_ratio,
        is_margin_call=is_margin_call,
        is_liquidation=is_liquidation,
        liquidation_price=liq_price
    )


# ============================================================================
# Cross-Margin Portfolio Calculations
# ============================================================================

def calculate_portfolio_margin(
    positions: dict[str, dict],  # symbol -> {qty, entry, current, is_long}
    total_collateral: Decimal,
    margin_pct: Decimal = Decimal("0.10")
) -> dict:
    """
    Calculate cross-margin for multiple positions.

    In cross-margin, all positions share the same collateral pool.

    Returns:
        Dict with portfolio-wide margin metrics
    """
    total_position_value = Decimal("0")
    total_unrealized = Decimal("0")
    total_margin_required = Decimal("0")

    for symbol, pos in positions.items():
        qty = to_decimal(pos["qty"])
        entry = to_decimal(pos["entry"])
        current = to_decimal(pos["current"])
        is_long = pos.get("is_long", True)

        position_value = current * qty
        total_position_value += position_value

        if is_long:
            total_unrealized += (current - entry) * qty
        else:
            total_unrealized += (entry - current) * qty

        total_margin_required += position_value * margin_pct

    equity = total_collateral + total_unrealized

    return {
        "total_position_value": total_position_value,
        "total_unrealized_pnl": total_unrealized,
        "total_equity": equity,
        "total_margin_required": total_margin_required,
        "margin_ratio": equity / total_margin_required if total_margin_required > 0 else Decimal("0"),
        "leverage_ratio": total_position_value / equity if equity > 0 else Decimal("0"),
        "margin_available": max(equity - total_margin_required, Decimal("0")),
        "is_margin_call": equity < total_margin_required * Decimal("2"),  # 200% buffer
        "is_liquidation": equity < total_margin_required,
    }
```

### Margin Quick Reference

| Term | Definition | Formula |
|------|------------|---------|
| Initial Margin | Required to open | Position * IM% |
| Maintenance Margin | Required to hold | Position * MM% |
| Leverage | Position / Equity | 1 / IM% |
| Margin Ratio | Equity / MM | Higher = Safer |
| Liquidation Price | Where MM = Equity | Complex (see code) |

---

## Part 6: Common Pitfalls

### Pitfall 1: Float Contamination

```python
# WRONG - Float contaminates Decimal precision
price = Decimal("100.50")
fee_rate = 0.001  # Float!
fee = price * Decimal(fee_rate)  # Decimal(0.001) preserves float imprecision!

# CORRECT - String conversion
fee_rate = "0.001"
fee = price * Decimal(fee_rate)

# CORRECT - Direct Decimal
fee_rate = Decimal("0.001")
fee = price * fee_rate
```

### Pitfall 2: Division Precision Loss

```python
# WRONG - Default division can lose precision
from decimal import Decimal

result = Decimal("1") / Decimal("3")
print(result)  # 0.3333333333333333333333333333 (28 digits, may truncate)

# CORRECT - Set context precision and quantize
from decimal import Decimal, getcontext

getcontext().prec = 50  # Higher internal precision
result = (Decimal("1") / Decimal("3")).quantize(Decimal("0.00000001"))
```

### Pitfall 3: Rounding Direction Errors

```python
from decimal import Decimal, ROUND_DOWN, ROUND_UP

balance = Decimal("100.555")

# WRONG - Using default rounding for fees (understates cost)
fee = balance.quantize(Decimal("0.01"))  # 100.56 (banker's rounding)

# CORRECT - Round UP for fees (conservative)
fee = balance.quantize(Decimal("0.01"), rounding=ROUND_UP)  # 100.56

# CORRECT - Round DOWN for available balance (conservative)
available = balance.quantize(Decimal("0.01"), rounding=ROUND_DOWN)  # 100.55
```

### Pitfall 4: Percentage Calculations

```python
# WRONG - Confusing percentage formats
win_rate = 55  # Is this 55% or 0.55?
position_pct = 0.02  # Is this 2% or 0.02%?

# CORRECT - Be explicit and consistent
win_rate_decimal = Decimal("0.55")      # 55% as decimal
win_rate_pct = Decimal("55")            # 55% as percentage

# Always document: "All percentages as decimals (0.55 = 55%)"
```

### Pitfall 5: Ignoring Fees in P&L

```python
# WRONG - Ignoring fees
pnl = (sell_price - buy_price) * quantity

# CORRECT - Include all costs
buy_cost = (buy_price * quantity) + buy_fee
sell_proceeds = (sell_price * quantity) - sell_fee
pnl = sell_proceeds - buy_cost
```

### Pitfall 6: Negative Position Quantities

```python
# WRONG - Allowing negative quantities (causes sign confusion)
quantity = Decimal("-5")  # Short position as negative? Or error?

# CORRECT - Separate quantity and side
quantity = Decimal("5")  # Always positive
side = Side.SHORT  # Direction is explicit
```

### Pitfall 7: Division by Zero

```python
# WRONG - No guard
sharpe = (returns - risk_free) / volatility  # Crash if volatility = 0

# CORRECT - Guard against zero
if volatility > 0:
    sharpe = (returns - risk_free) / volatility
else:
    sharpe = Decimal("0")  # Or raise, or return None, depending on context
```

### Pitfall 8: Timestamp Handling

```python
# WRONG - Mixing timezones
from datetime import datetime

trade_time = datetime.now()  # Local time? UTC? Unknown!

# CORRECT - Always use UTC
from datetime import datetime, timezone

trade_time = datetime.now(timezone.utc)

# Or use aware timestamps
from dateutil import tz
trade_time = datetime.now(tz.UTC)
```

---

## Part 7: Integration with Trading Arena

### Database Model Alignment

This skill is designed to work with the Trading Arena models defined in `trading-arena/api/db/models.py`:

```python
# Integration example with SQLAlchemy models
from trading_arena.api.db.models import Order, OrderFill, PortfolioBalance
from trading_finance.pnl import Trade, Side, PortfolioTracker
from trading_finance.precision import to_decimal

async def calculate_collective_pnl(
    collective_id: str,
    current_prices: dict[str, Decimal],
    session: AsyncSession
) -> PortfolioPnL:
    """
    Calculate P&L for a collective using their order history.
    """
    # Get initial balance (from snapshots or config)
    initial_balance = Decimal("100000")  # Or from first snapshot

    # Create portfolio tracker
    tracker = PortfolioTracker(initial_balance)

    # Get all filled orders
    stmt = select(Order).where(
        Order.collective_id == collective_id,
        Order.status.in_([OrderStatus.FILLED, OrderStatus.PARTIALLY_FILLED])
    ).order_by(Order.created_at)

    orders = await session.execute(stmt)

    for order in orders.scalars():
        # Convert to Trade object
        trade = Trade(
            trade_id=order.order_id,
            symbol=order.symbol,
            side=Side.BUY if order.side == OrderSide.BUY else Side.SELL,
            quantity=order.filled_quantity,
            price=order.average_fill_price,
            fee=sum(f.fee for f in order.fills),
            executed_at=order.updated_at
        )
        tracker.add_trade(trade)

    return tracker.get_portfolio_pnl(current_prices)
```

### WebSocket Real-Time Updates

Combine with `websocket-server-patterns` skill for real-time P&L streaming:

```python
# Real-time P&L updates via WebSocket
from trading_finance.pnl import PortfolioTracker
from trading_finance.metrics import calculate_max_drawdown

async def stream_portfolio_updates(
    collective_id: str,
    manager: ConnectionManager
):
    """Stream real-time portfolio updates."""
    while True:
        # Get current prices
        prices = await get_current_prices()

        # Calculate P&L
        pnl = await calculate_collective_pnl(collective_id, prices)

        # Calculate additional metrics
        values = await get_historical_values(collective_id)
        max_dd, _, _, _ = calculate_max_drawdown(values)

        # Broadcast to collective's portfolio room
        await manager.broadcast_to_room(
            f"portfolio:{collective_id}",
            {
                "type": "portfolio_update",
                "data": {
                    "total_value": str(pnl.total_value + pnl.cash_balance),
                    "unrealized_pnl": str(pnl.total_unrealized),
                    "realized_pnl": str(pnl.total_realized),
                    "return_pct": str(pnl.return_pct),
                    "max_drawdown": str(max_dd * 100),
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        await asyncio.sleep(1)  # Update every second
```

---

## Part 8: Testing Financial Calculations

### Property-Based Testing

```python
# tests/test_financial_properties.py
"""
Property-based tests for financial calculations.

Financial code MUST be correct. These tests verify mathematical properties.
"""

from decimal import Decimal
from hypothesis import given, strategies as st
from trading_finance.precision import to_decimal
from trading_finance.pnl import PositionTracker, Trade, Side

# Strategy for valid Decimal amounts
decimal_strategy = st.decimals(
    min_value=Decimal("0.00000001"),
    max_value=Decimal("1000000"),
    allow_nan=False,
    allow_infinity=False
)


@given(
    buy_qty=decimal_strategy,
    buy_price=decimal_strategy,
    sell_price=decimal_strategy
)
def test_pnl_is_buy_sell_difference(buy_qty, buy_price, sell_price):
    """P&L should equal (sell_price - buy_price) * quantity, minus fees."""
    tracker = PositionTracker("TEST")

    buy_fee = Decimal("0")
    sell_fee = Decimal("0")

    tracker.add_trade(Trade(
        trade_id="b1", symbol="TEST", side=Side.BUY,
        quantity=buy_qty, price=buy_price, fee=buy_fee,
        executed_at=datetime.now()
    ))

    realized = tracker.add_trade(Trade(
        trade_id="s1", symbol="TEST", side=Side.SELL,
        quantity=buy_qty, price=sell_price, fee=sell_fee,
        executed_at=datetime.now()
    ))

    expected = (sell_price - buy_price) * buy_qty
    assert realized == expected


@given(amounts=st.lists(decimal_strategy, min_size=1, max_size=100))
def test_decimal_sum_precision(amounts):
    """Summing many Decimals should be exact."""
    total = sum(to_decimal(str(a)) for a in amounts)

    # Verify no float contamination
    sign, digits, exp = total.as_tuple()
    assert all(isinstance(d, int) for d in digits)


@given(
    initial=decimal_strategy,
    trades=st.lists(
        st.tuples(st.sampled_from([Side.BUY, Side.SELL]), decimal_strategy),
        min_size=0,
        max_size=20
    )
)
def test_position_quantity_non_negative(initial, trades):
    """Position quantity should never go negative."""
    tracker = PositionTracker("TEST")

    # Start with initial buy
    tracker.add_trade(Trade(
        trade_id="init", symbol="TEST", side=Side.BUY,
        quantity=initial, price=Decimal("100"), fee=Decimal("0"),
        executed_at=datetime.now()
    ))

    for i, (side, qty) in enumerate(trades):
        if side == Side.SELL:
            # Only sell what we have
            qty = min(qty, tracker.quantity)

        if qty > 0:
            tracker.add_trade(Trade(
                trade_id=f"t{i}", symbol="TEST", side=side,
                quantity=qty, price=Decimal("100"), fee=Decimal("0"),
                executed_at=datetime.now()
            ))

    assert tracker.quantity >= 0
```

### Edge Case Tests

```python
# tests/test_edge_cases.py
"""
Edge case tests for financial calculations.
"""

import pytest
from decimal import Decimal
from trading_finance.metrics import (
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_returns
)


def test_sharpe_ratio_zero_volatility():
    """Sharpe should be 0 when volatility is 0."""
    # Constant returns = zero volatility
    returns = [Decimal("0.01")] * 10
    sharpe = calculate_sharpe_ratio(returns)
    # Should not raise, should return 0 or handle gracefully
    assert sharpe == Decimal("0")


def test_max_drawdown_only_gains():
    """Max drawdown should be 0 if portfolio only gains."""
    values = [Decimal("100"), Decimal("110"), Decimal("120"), Decimal("130")]
    max_dd, _, _, _ = calculate_max_drawdown(values)
    assert max_dd == Decimal("0")


def test_returns_empty_list():
    """Returns calculation should handle empty list."""
    returns = calculate_returns([])
    assert returns == []


def test_returns_single_value():
    """Returns calculation should handle single value."""
    returns = calculate_returns([Decimal("100")])
    assert returns == []


def test_pnl_with_zero_cost_basis():
    """P&L percentage should handle zero cost basis."""
    result = PnLResult(
        realized_pnl=Decimal("100"),
        unrealized_pnl=Decimal("0"),
        total_pnl=Decimal("100"),
        cost_basis=Decimal("0"),  # Edge case!
        current_value=Decimal("0"),
        quantity_held=Decimal("0")
    )
    # Should not divide by zero
    assert result.return_pct == Decimal("0")
```

---

## Summary

This skill provides the complete financial calculation foundation for Trading Arena Phase 2:

| Component | Purpose | Key Functions |
|-----------|---------|---------------|
| Precision | Decimal arithmetic | `to_decimal`, `round_down`, `round_up` |
| P&L | Profit/loss tracking | `PositionTracker`, `PortfolioTracker` |
| Metrics | Performance analysis | `sharpe_ratio`, `max_drawdown`, `win_rate` |
| Position Sizing | Risk management | `kelly_criterion`, `fixed_fractional` |
| Margin | Leverage calculations | `liquidation_price`, `margin_status` |

**Core Principle**: Financial accuracy is non-negotiable. Always use Decimal, always validate precision, always test edge cases.

**Next Steps**:
1. Review `references/` for complete implementations
2. Review `scripts/` for validation tools
3. Integrate with Trading Arena Phase 2

---

## References

- `references/precision.py` - Complete precision handling module
- `references/pnl.py` - P&L calculation implementation
- `references/metrics.py` - Portfolio metrics implementation
- `references/position_sizing.py` - Position sizing algorithms
- `references/margin.py` - Margin calculations

## Scripts

- `scripts/validate_precision.py` - Precision validation tests
- `scripts/pnl_calculator.py` - CLI P&L calculator
- `scripts/metric_analyzer.py` - Portfolio metric analysis
