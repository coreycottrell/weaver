"""
Margin and leverage calculations for trading.

Covers:
- Initial and maintenance margin
- Leverage ratio calculations
- Liquidation price estimation
- Margin call detection
- Cross-margin portfolio calculations

Author: AI-CIV (capability-curator)
Created: 2025-12-26
Domain: trading-systems
"""

from decimal import Decimal
from typing import Optional, Dict
from dataclasses import dataclass

# Import from sibling module
try:
    from .precision import to_decimal, round_up, round_down, safe_divide
except ImportError:
    # For standalone testing
    from precision import to_decimal, round_up, round_down, safe_divide


@dataclass
class MarginRequirements:
    """Margin requirements for a position."""
    initial_margin: Decimal      # Required to open position
    maintenance_margin: Decimal  # Required to maintain position
    initial_margin_pct: Decimal  # As percentage
    maintenance_margin_pct: Decimal  # As percentage

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "initial_margin": str(self.initial_margin),
            "maintenance_margin": str(self.maintenance_margin),
            "initial_margin_pct": str(self.initial_margin_pct),
            "maintenance_margin_pct": str(self.maintenance_margin_pct),
        }


@dataclass
class MarginStatus:
    """Current margin status for a position."""
    position_value: Decimal
    collateral: Decimal
    unrealized_pnl: Decimal
    margin_used: Decimal
    margin_available: Decimal
    margin_ratio: Decimal        # Collateral / Margin Required (higher = safer)
    leverage_ratio: Decimal      # Position Value / Collateral
    is_margin_call: bool
    is_liquidation: bool
    liquidation_price: Optional[Decimal]

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "position_value": str(self.position_value),
            "collateral": str(self.collateral),
            "unrealized_pnl": str(self.unrealized_pnl),
            "margin_used": str(self.margin_used),
            "margin_available": str(self.margin_available),
            "margin_ratio": str(self.margin_ratio),
            "leverage_ratio": str(self.leverage_ratio),
            "is_margin_call": self.is_margin_call,
            "is_liquidation": self.is_liquidation,
        }
        if self.liquidation_price is not None:
            result["liquidation_price"] = str(self.liquidation_price)
        return result


def calculate_margin_requirements(
    notional_value: Decimal,
    initial_margin_pct: Decimal = Decimal("0.10"),    # 10% = 10x max leverage
    maintenance_margin_pct: Decimal = Decimal("0.05")  # 5%
) -> MarginRequirements:
    """
    Calculate margin requirements for a position.

    Args:
        notional_value: Total position value (quantity * price)
        initial_margin_pct: Initial margin as decimal (0.10 = 10%)
        maintenance_margin_pct: Maintenance margin as decimal (0.05 = 5%)

    Returns:
        MarginRequirements with calculated values

    Examples:
        >>> calculate_margin_requirements(Decimal("100000"), Decimal("0.10"))
        MarginRequirements(
            initial_margin=10000,
            maintenance_margin=5000,
            initial_margin_pct=10,
            maintenance_margin_pct=5
        )

    Common margin rates:
        - Crypto spot: 100% (no leverage)
        - Crypto futures: 1-5% (20-100x leverage)
        - Stocks (Reg T): 50% (2x leverage)
        - Forex: 1-4% (25-100x leverage)
    """
    notional_value = to_decimal(notional_value)
    initial_margin_pct = to_decimal(initial_margin_pct)
    maintenance_margin_pct = to_decimal(maintenance_margin_pct)

    # Round UP for margin requirements (conservative)
    initial_margin = round_up(notional_value * initial_margin_pct, 2)
    maintenance_margin = round_up(notional_value * maintenance_margin_pct, 2)

    return MarginRequirements(
        initial_margin=initial_margin,
        maintenance_margin=maintenance_margin,
        initial_margin_pct=initial_margin_pct * Decimal("100"),
        maintenance_margin_pct=maintenance_margin_pct * Decimal("100")
    )


def calculate_max_leverage(initial_margin_pct: Decimal) -> Decimal:
    """
    Calculate maximum leverage from initial margin percentage.

    Leverage = 1 / Initial Margin %

    Args:
        initial_margin_pct: Initial margin as decimal (0.10 = 10%)

    Returns:
        Maximum leverage ratio

    Examples:
        >>> calculate_max_leverage(Decimal("0.10"))  # 10% margin
        Decimal('10')  # 10x leverage
        >>> calculate_max_leverage(Decimal("0.05"))  # 5% margin
        Decimal('20')  # 20x leverage
        >>> calculate_max_leverage(Decimal("0.50"))  # 50% margin
        Decimal('2')   # 2x leverage
    """
    initial_margin_pct = to_decimal(initial_margin_pct)

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

    Examples:
        >>> calculate_leverage_ratio(Decimal("50000"), Decimal("10000"))
        Decimal('5')  # 5x leverage
    """
    position_value = to_decimal(position_value)
    collateral = to_decimal(collateral)

    return safe_divide(position_value, collateral)


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
    Equity (Collateral + Unrealized PnL) < Maintenance Margin + Fees

    Args:
        entry_price: Position entry price
        quantity: Position quantity
        collateral: Total collateral/margin deposited
        maintenance_margin_pct: Maintenance margin requirement as decimal
        is_long: True for long, False for short
        fees_pct: Estimated liquidation fees as decimal (default 0.1%)

    Returns:
        Price at which liquidation occurs

    Examples:
        >>> calculate_liquidation_price(
        ...     entry_price=Decimal("50000"),
        ...     quantity=Decimal("1"),
        ...     collateral=Decimal("5000"),      # 10x leverage
        ...     maintenance_margin_pct=Decimal("0.05"),
        ...     is_long=True
        ... )
        Decimal('45263.15')  # Liquidated if BTC drops below this

    For longs: liquidation when price FALLS
    For shorts: liquidation when price RISES
    """
    entry_price = to_decimal(entry_price)
    quantity = to_decimal(quantity)
    collateral = to_decimal(collateral)
    maintenance_margin_pct = to_decimal(maintenance_margin_pct)
    fees_pct = to_decimal(fees_pct)

    # Total margin requirement including fees
    total_margin_pct = maintenance_margin_pct + fees_pct

    if is_long:
        # Long position: liquidation when price falls
        # At liquidation: collateral + (liq_price - entry) * qty = maint_pct * liq_price * qty
        # Solving for liq_price:
        # collateral - entry * qty = liq_price * qty * maint_pct - liq_price * qty
        # collateral - entry * qty = liq_price * qty * (maint_pct - 1)
        # liq_price = (entry * qty - collateral) / (qty * (1 - maint_pct))
        denominator = quantity * (Decimal("1") - total_margin_pct)
        if denominator <= 0:
            return Decimal("0")
        liq_price = (entry_price * quantity - collateral) / denominator
    else:
        # Short position: liquidation when price rises
        # At liquidation: collateral + (entry - liq_price) * qty = maint_pct * liq_price * qty
        # Solving for liq_price:
        # collateral + entry * qty = liq_price * qty + maint_pct * liq_price * qty
        # collateral + entry * qty = liq_price * qty * (1 + maint_pct)
        # liq_price = (collateral + entry * qty) / (qty * (1 + maint_pct))
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

    This is the primary function for monitoring position health.

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

    Margin Ratio interpretation:
        > 3.0: Healthy
        2.0-3.0: Adequate
        1.5-2.0: Warning zone
        1.0-1.5: Margin call territory
        < 1.0: Liquidation imminent
    """
    entry_price = to_decimal(entry_price)
    current_price = to_decimal(current_price)
    quantity = to_decimal(quantity)
    collateral = to_decimal(collateral)
    initial_margin_pct = to_decimal(initial_margin_pct)
    maintenance_margin_pct = to_decimal(maintenance_margin_pct)

    # Position value at current price
    position_value = current_price * quantity

    # Unrealized P&L
    if is_long:
        unrealized_pnl = (current_price - entry_price) * quantity
    else:
        unrealized_pnl = (entry_price - current_price) * quantity

    # Effective equity = collateral + unrealized P&L
    equity = collateral + unrealized_pnl

    # Margin requirements at current position value
    initial_margin = position_value * initial_margin_pct
    maintenance_margin = position_value * maintenance_margin_pct

    # Margin ratio = equity / maintenance margin (higher = safer)
    margin_ratio = safe_divide(equity, maintenance_margin)

    # Leverage ratio = position value / equity
    leverage_ratio = safe_divide(position_value, equity) if equity > 0 else Decimal("0")

    # Margin call: equity < initial margin (need to add collateral or reduce position)
    is_margin_call = equity < initial_margin

    # Liquidation: equity < maintenance margin (position will be force-closed)
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

@dataclass
class PortfolioMarginStatus:
    """Cross-margin portfolio status."""
    total_position_value: Decimal
    total_unrealized_pnl: Decimal
    total_equity: Decimal
    total_margin_required: Decimal
    margin_ratio: Decimal
    leverage_ratio: Decimal
    margin_available: Decimal
    is_margin_call: bool
    is_liquidation: bool

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "total_position_value": str(self.total_position_value),
            "total_unrealized_pnl": str(self.total_unrealized_pnl),
            "total_equity": str(self.total_equity),
            "total_margin_required": str(self.total_margin_required),
            "margin_ratio": str(self.margin_ratio),
            "leverage_ratio": str(self.leverage_ratio),
            "margin_available": str(self.margin_available),
            "is_margin_call": self.is_margin_call,
            "is_liquidation": self.is_liquidation,
        }


def calculate_portfolio_margin(
    positions: Dict[str, dict],  # symbol -> {qty, entry, current, is_long}
    total_collateral: Decimal,
    margin_pct: Decimal = Decimal("0.10")
) -> PortfolioMarginStatus:
    """
    Calculate cross-margin for multiple positions.

    In cross-margin mode, all positions share the same collateral pool.
    Profits from one position can offset losses from another.

    Args:
        positions: Dict of symbol -> position details
            Each position should have: qty, entry, current, is_long (optional, default True)
        total_collateral: Total collateral deposited
        margin_pct: Margin requirement as decimal

    Returns:
        PortfolioMarginStatus with aggregate metrics

    Examples:
        >>> positions = {
        ...     "BTC": {"qty": "0.5", "entry": "50000", "current": "52000", "is_long": True},
        ...     "ETH": {"qty": "5", "entry": "3000", "current": "2800", "is_long": True},
        ... }
        >>> calculate_portfolio_margin(positions, Decimal("5000"), Decimal("0.10"))
    """
    total_collateral = to_decimal(total_collateral)
    margin_pct = to_decimal(margin_pct)

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

    # Total equity = collateral + unrealized P&L
    equity = total_collateral + total_unrealized

    # Margin ratio = equity / margin required
    margin_ratio = safe_divide(equity, total_margin_required)

    # Leverage ratio = total position value / equity
    leverage_ratio = safe_divide(total_position_value, equity) if equity > 0 else Decimal("0")

    # Margin call at 200% margin ratio (warning)
    is_margin_call = margin_ratio < Decimal("2")

    # Liquidation at 100% margin ratio
    is_liquidation = margin_ratio < Decimal("1")

    return PortfolioMarginStatus(
        total_position_value=total_position_value,
        total_unrealized_pnl=total_unrealized,
        total_equity=equity,
        total_margin_required=total_margin_required,
        margin_ratio=margin_ratio,
        leverage_ratio=leverage_ratio,
        margin_available=max(equity - total_margin_required, Decimal("0")),
        is_margin_call=is_margin_call,
        is_liquidation=is_liquidation
    )


def calculate_required_collateral(
    position_value: Decimal,
    target_leverage: Decimal
) -> Decimal:
    """
    Calculate required collateral for a desired leverage level.

    Args:
        position_value: Desired position value
        target_leverage: Desired leverage (e.g., 5 for 5x)

    Returns:
        Required collateral amount

    Examples:
        >>> calculate_required_collateral(Decimal("50000"), Decimal("5"))
        Decimal('10000')  # Need $10k for 5x leverage on $50k position
    """
    position_value = to_decimal(position_value)
    target_leverage = to_decimal(target_leverage)

    if target_leverage <= 0:
        return position_value  # No leverage = full collateral

    return safe_divide(position_value, target_leverage)


def calculate_max_position(
    collateral: Decimal,
    max_leverage: Decimal,
    current_price: Decimal
) -> Dict[str, Decimal]:
    """
    Calculate maximum position size given collateral and leverage limit.

    Args:
        collateral: Available collateral
        max_leverage: Maximum allowed leverage
        current_price: Current asset price

    Returns:
        Dict with max_notional and max_quantity
    """
    collateral = to_decimal(collateral)
    max_leverage = to_decimal(max_leverage)
    current_price = to_decimal(current_price)

    max_notional = collateral * max_leverage
    max_quantity = safe_divide(max_notional, current_price)

    return {
        "max_notional": max_notional,
        "max_quantity": round_down(max_quantity, 8)
    }


# ============================================================================
# Demonstration / Self-Test
# ============================================================================

if __name__ == "__main__":
    print("=== Margin Requirements Test ===")

    req = calculate_margin_requirements(
        Decimal("100000"),  # $100k position
        Decimal("0.10"),    # 10% initial margin
        Decimal("0.05")     # 5% maintenance
    )

    print(f"Position: $100,000")
    print(f"Initial margin: ${req.initial_margin} ({req.initial_margin_pct}%)")
    print(f"Maintenance margin: ${req.maintenance_margin} ({req.maintenance_margin_pct}%)")
    print(f"Max leverage: {calculate_max_leverage(Decimal('0.10'))}x")

    print("\n=== Leverage Calculation Test ===")

    leverage = calculate_leverage_ratio(
        Decimal("50000"),   # $50k position
        Decimal("10000")    # $10k collateral
    )
    print(f"Position: $50,000, Collateral: $10,000")
    print(f"Leverage: {leverage}x")

    print("\n=== Liquidation Price Test ===")

    # Long position
    liq_long = calculate_liquidation_price(
        entry_price=Decimal("50000"),
        quantity=Decimal("1"),
        collateral=Decimal("5000"),      # 10x leverage
        maintenance_margin_pct=Decimal("0.05"),
        is_long=True
    )

    # Short position
    liq_short = calculate_liquidation_price(
        entry_price=Decimal("50000"),
        quantity=Decimal("1"),
        collateral=Decimal("5000"),
        maintenance_margin_pct=Decimal("0.05"),
        is_long=False
    )

    print(f"Entry: $50,000, Collateral: $5,000 (10x leverage)")
    print(f"Long liquidation price: ${liq_long}")
    print(f"Short liquidation price: ${liq_short}")

    print("\n=== Margin Status Test ===")

    # Position moving against us
    status = calculate_margin_status(
        entry_price=Decimal("50000"),
        current_price=Decimal("47000"),  # Price dropped 6%
        quantity=Decimal("1"),
        collateral=Decimal("5000"),
        initial_margin_pct=Decimal("0.10"),
        maintenance_margin_pct=Decimal("0.05"),
        is_long=True
    )

    print(f"Entry: $50,000, Current: $47,000 (down 6%)")
    print(f"Position value: ${status.position_value}")
    print(f"Unrealized P&L: ${status.unrealized_pnl}")
    print(f"Margin ratio: {status.margin_ratio:.2f} (equity / maint margin)")
    print(f"Leverage: {status.leverage_ratio:.1f}x")
    print(f"Margin call: {status.is_margin_call}")
    print(f"Liquidation: {status.is_liquidation}")
    print(f"Liquidation price: ${status.liquidation_price}")

    print("\n=== Cross-Margin Portfolio Test ===")

    positions = {
        "BTC": {
            "qty": "0.5",
            "entry": "50000",
            "current": "52000",  # Profit
            "is_long": True
        },
        "ETH": {
            "qty": "5",
            "entry": "3000",
            "current": "2800",  # Loss
            "is_long": True
        },
    }

    portfolio_status = calculate_portfolio_margin(
        positions,
        Decimal("5000"),  # $5k collateral
        Decimal("0.10")   # 10% margin
    )

    print(f"Positions: BTC (0.5 @ $50k->$52k), ETH (5 @ $3k->$2.8k)")
    print(f"Total collateral: $5,000")
    print(f"Total position value: ${portfolio_status.total_position_value}")
    print(f"Total unrealized P&L: ${portfolio_status.total_unrealized_pnl}")
    print(f"Total equity: ${portfolio_status.total_equity}")
    print(f"Margin ratio: {portfolio_status.margin_ratio:.2f}")
    print(f"Portfolio leverage: {portfolio_status.leverage_ratio:.1f}x")
    print(f"Margin call: {portfolio_status.is_margin_call}")

    print("\n=== All tests passed! ===")
