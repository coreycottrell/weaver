"""
Profit and Loss calculations for trading systems.

Supports:
- Per-trade P&L
- Position P&L (multiple trades aggregated)
- Portfolio P&L (multiple positions)
- FIFO, LIFO, and average cost basis methods

Author: AI-CIV (capability-curator)
Created: 2025-12-26
Domain: trading-systems
"""

from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum

# Import from sibling module
try:
    from .precision import to_decimal, round_down, PRICE_PRECISION
except ImportError:
    # For standalone testing
    from precision import to_decimal, round_down, PRICE_PRECISION


class Side(Enum):
    """Order side (buy/sell)."""
    BUY = "buy"
    SELL = "sell"


class CostBasisMethod(Enum):
    """Cost basis calculation method."""
    FIFO = "fifo"      # First In, First Out
    LIFO = "lifo"      # Last In, First Out
    AVERAGE = "average"  # Weighted average cost


@dataclass
class Trade:
    """
    Individual trade execution.

    Represents a single fill/execution of an order.
    """
    trade_id: str
    symbol: str
    side: Side
    quantity: Decimal
    price: Decimal
    fee: Decimal
    executed_at: datetime

    def __post_init__(self):
        """Validate and convert fields to Decimal."""
        self.quantity = to_decimal(self.quantity)
        self.price = to_decimal(self.price)
        self.fee = to_decimal(self.fee)

    @property
    def notional(self) -> Decimal:
        """Total value of trade (quantity * price)."""
        return self.quantity * self.price

    @property
    def cost(self) -> Decimal:
        """
        Total cost including fees (for buys).

        For BUYS: notional + fee (you pay more)
        For SELLS: notional + fee (used for cost calculation, not proceeds)
        """
        return self.notional + self.fee

    @property
    def proceeds(self) -> Decimal:
        """
        Net proceeds after fees (for sells).

        For SELLS: notional - fee (you receive less)
        """
        return self.notional - self.fee

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "quantity": str(self.quantity),
            "price": str(self.price),
            "fee": str(self.fee),
            "executed_at": self.executed_at.isoformat(),
        }


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

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "realized_pnl": str(self.realized_pnl),
            "unrealized_pnl": str(self.unrealized_pnl),
            "total_pnl": str(self.total_pnl),
            "cost_basis": str(self.cost_basis),
            "current_value": str(self.current_value),
            "quantity_held": str(self.quantity_held),
            "return_pct": str(self.return_pct),
            "win_count": self.win_count,
            "loss_count": self.loss_count,
            "total_trades": self.total_trades,
            "win_rate": str(self.win_rate),
        }


class PositionTracker:
    """
    Track position and calculate P&L for a single symbol.

    Supports multiple cost basis methods:
    - FIFO: First lots bought are first sold (common for tax purposes)
    - LIFO: Last lots bought are first sold
    - AVERAGE: Weighted average cost of all purchases

    Usage:
        tracker = PositionTracker("BTC", CostBasisMethod.FIFO)
        tracker.add_trade(buy_trade)
        tracker.add_trade(sell_trade)  # Returns realized P&L
        result = tracker.get_pnl_result(current_price)
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
        self.lots: List[Tuple[Decimal, Decimal]] = []

        # P&L tracking
        self.realized_pnl: Decimal = Decimal("0")
        self.total_fees: Decimal = Decimal("0")
        self.trades: List[Trade] = []
        self.win_count: int = 0
        self.loss_count: int = 0

    def add_trade(self, trade: Trade) -> Decimal:
        """
        Process a trade and return realized P&L (if any).

        Args:
            trade: Trade to process

        Returns:
            Realized P&L from this trade (Decimal(0) if opening/adding)

        Raises:
            ValueError: If trade symbol doesn't match position
            ValueError: If selling more than held
        """
        if trade.symbol != self.symbol:
            raise ValueError(
                f"Trade symbol {trade.symbol} doesn't match position {self.symbol}"
            )

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

        Args:
            quantity_to_sell: Amount to sell

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

        current_value = self.quantity * to_decimal(current_price)
        return current_value - self.cost_basis

    def get_pnl_result(self, current_price: Decimal) -> PnLResult:
        """
        Get complete P&L breakdown.

        Args:
            current_price: Current market price

        Returns:
            PnLResult with all P&L metrics
        """
        current_price = to_decimal(current_price)
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

    def to_dict(self) -> dict:
        """Convert tracker state to dictionary."""
        return {
            "symbol": self.symbol,
            "method": self.method.value,
            "quantity": str(self.quantity),
            "cost_basis": str(self.cost_basis),
            "average_cost": str(self.average_cost),
            "realized_pnl": str(self.realized_pnl),
            "total_fees": str(self.total_fees),
            "win_count": self.win_count,
            "loss_count": self.loss_count,
            "trade_count": len(self.trades),
        }


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

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "total_realized": str(self.total_realized),
            "total_unrealized": str(self.total_unrealized),
            "total_pnl": str(self.total_pnl),
            "total_cost_basis": str(self.total_cost_basis),
            "total_value": str(self.total_value),
            "cash_balance": str(self.cash_balance),
            "return_pct": str(self.return_pct),
            "portfolio_value": str(self.total_value + self.cash_balance),
            "positions": {k: v.to_dict() for k, v in self.positions.items()},
        }


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

        Args:
            trade: Trade to process

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
            price = to_decimal(current_prices.get(symbol, Decimal("0")))
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
            return_pct = (
                (portfolio_value - self.initial_cash) / self.initial_cash
            ) * Decimal("100")

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

    def get_trade_history(self) -> List[Trade]:
        """Get all trades across all positions."""
        all_trades = []
        for tracker in self.positions.values():
            all_trades.extend(tracker.trades)
        return sorted(all_trades, key=lambda t: t.executed_at)

    def get_realized_pnl_list(self) -> List[Decimal]:
        """
        Get list of realized P&L per trade.

        Useful for calculating trade statistics (win rate, etc.)
        """
        pnls = []
        for tracker in self.positions.values():
            # Replay trades to get individual P&Ls
            temp_tracker = PositionTracker(tracker.symbol, tracker.method)
            for trade in tracker.trades:
                pnl = temp_tracker.add_trade(trade)
                if trade.side == Side.SELL:
                    pnls.append(pnl)
        return pnls

    def to_dict(self) -> dict:
        """Convert portfolio state to dictionary."""
        return {
            "initial_cash": str(self.initial_cash),
            "current_cash": str(self.cash),
            "method": self.method.value,
            "positions": {k: v.to_dict() for k, v in self.positions.items()},
        }


# ============================================================================
# Demonstration / Self-Test
# ============================================================================

if __name__ == "__main__":
    from datetime import datetime

    print("=== Single Position P&L Test ===")
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
    print(f"After buy1: qty={tracker.quantity}, cost={tracker.cost_basis}")

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
    print(f"After buy2: qty={tracker.quantity}, cost={tracker.cost_basis}")
    print(f"Average cost: ${tracker.average_cost}")

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
    print(f"Sell realized P&L: ${realized}")

    # Get current P&L at $46,000
    result = tracker.get_pnl_result(Decimal("46000"))
    print(f"\nP&L Result at $46,000:")
    print(f"  Realized: ${result.realized_pnl}")
    print(f"  Unrealized: ${result.unrealized_pnl}")
    print(f"  Total P&L: ${result.total_pnl}")
    print(f"  Remaining: {result.quantity_held} BTC")

    print("\n=== Portfolio P&L Test ===")
    portfolio = PortfolioTracker(initial_cash=Decimal("100000"))

    # Add same BTC trades
    portfolio.add_trade(buy1)
    portfolio.add_trade(buy2)
    portfolio.add_trade(sell1)

    # Add ETH trade
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
    print(f"Cash: ${pnl.cash_balance}")
    print(f"Positions Value: ${pnl.total_value}")
    print(f"Total Return: {pnl.return_pct}%")
    print(f"Realized P&L: ${pnl.total_realized}")
    print(f"Unrealized P&L: ${pnl.total_unrealized}")

    print("\n=== All tests passed! ===")
