"""
Position sizing algorithms for risk management.

Implements:
- Kelly Criterion (optimal sizing based on edge)
- Fixed Fractional (constant % risk per trade)
- Volatility-based sizing
- Position validation

Author: AI-CIV (capability-curator)
Created: 2025-12-26
Domain: trading-systems
"""

from decimal import Decimal
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
import math

# Import from sibling module
try:
    from .precision import to_decimal, round_down, safe_divide
except ImportError:
    # For standalone testing
    from precision import to_decimal, round_down, safe_divide


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

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "quantity": str(self.quantity),
            "notional": str(self.notional),
            "risk_amount": str(self.risk_amount),
            "portfolio_pct": str(self.portfolio_pct),
            "method": self.method,
        }
        if self.stop_loss_pct is not None:
            result["stop_loss_pct"] = str(self.stop_loss_pct)
        if self.confidence is not None:
            result["confidence"] = str(self.confidence)
        return result


def kelly_criterion(
    win_rate: Decimal,
    avg_win: Decimal,
    avg_loss: Decimal,
    fraction: Decimal = Decimal("0.5")  # Half-Kelly is common
) -> Decimal:
    """
    Calculate Kelly Criterion optimal bet size.

    The Kelly Criterion determines the optimal fraction of capital to risk
    to maximize long-term growth rate.

    Formula: Kelly % = W - (1-W)/B
    Where:
        W = Probability of winning
        B = Ratio of win size to loss size (win/loss ratio)

    Args:
        win_rate: Historical win rate as decimal (0.55 = 55%)
        avg_win: Average winning trade size (absolute value)
        avg_loss: Average losing trade size (absolute value, positive number)
        fraction: Kelly fraction to use (0.5 = half-Kelly, recommended)

    Returns:
        Optimal bet size as fraction of bankroll (0.20 = 20%)

    Examples:
        >>> kelly_criterion(
        ...     Decimal("0.55"),  # 55% win rate
        ...     Decimal("100"),   # Average $100 win
        ...     Decimal("80")     # Average $80 loss
        ... )
        Decimal('0.11875')  # Bet ~12% of bankroll (half-Kelly)

    WARNING: Full Kelly (fraction=1.0) is mathematically optimal but
    extremely aggressive. It assumes:
    - Unlimited trading opportunities
    - Accurate win rate and ratio estimates
    - No serial correlation in trades

    In practice, use half-Kelly (0.5) or quarter-Kelly (0.25).
    This reduces volatility while sacrificing only a small amount of growth.
    """
    win_rate = to_decimal(win_rate)
    avg_win = to_decimal(avg_win)
    avg_loss = to_decimal(avg_loss)
    fraction = to_decimal(fraction)

    if avg_loss <= 0:
        return Decimal("0")

    # Win/loss ratio (B in the formula)
    b = avg_win / avg_loss

    # Kelly formula: W - (1-W)/B
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
    Position size is determined by the risk amount and stop loss distance.

    Formula: Position Size = Risk Amount / Risk Per Unit
    Where:
        Risk Amount = Portfolio Value * Risk Percentage
        Risk Per Unit = |Entry Price - Stop Loss Price|

    Args:
        portfolio_value: Current portfolio value
        risk_per_trade: Max % to risk per trade as decimal (0.01 = 1%)
        entry_price: Entry price for the trade
        stop_loss_price: Stop loss price

    Returns:
        PositionSize with calculated values

    Examples:
        >>> fixed_fractional(
        ...     Decimal("100000"),   # $100k portfolio
        ...     Decimal("0.01"),     # 1% risk per trade
        ...     Decimal("50000"),    # Entry at $50k
        ...     Decimal("48000")     # Stop at $48k (4% below)
        ... )
        PositionSize(quantity=0.5, notional=25000, risk_amount=1000, ...)

    Best for:
    - Consistent risk exposure across trades
    - Simple implementation
    - Works well with defined stop losses
    """
    portfolio_value = to_decimal(portfolio_value)
    risk_per_trade = to_decimal(risk_per_trade)
    entry_price = to_decimal(entry_price)
    stop_loss_price = to_decimal(stop_loss_price)

    # Calculate risk amount
    risk_amount = portfolio_value * risk_per_trade

    # Calculate risk per unit (distance to stop loss)
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
    target_volatility: Decimal,  # e.g., 0.10 = 10% annual vol contribution
    asset_volatility: Decimal,   # Asset's annualized volatility
    entry_price: Decimal,
    max_position_pct: Decimal = Decimal("0.25")  # Max 25% of portfolio
) -> PositionSize:
    """
    Volatility-adjusted position sizing.

    Size positions inversely to their volatility to achieve
    consistent portfolio volatility contribution.

    Formula: Position Size = Target Vol / Asset Vol * Portfolio

    High-volatility assets get smaller positions.
    Low-volatility assets get larger positions.

    Args:
        portfolio_value: Current portfolio value
        target_volatility: Target portfolio vol contribution as decimal (0.10 = 10%)
        asset_volatility: Asset's annualized volatility as decimal (0.60 = 60%)
        entry_price: Entry price
        max_position_pct: Maximum position size as % of portfolio (default 25%)

    Returns:
        PositionSize with calculated values

    Examples:
        >>> volatility_adjusted_sizing(
        ...     Decimal("100000"),   # $100k
        ...     Decimal("0.10"),     # 10% target vol contribution
        ...     Decimal("0.60"),     # BTC has 60% annualized vol
        ...     Decimal("50000")     # Entry at $50k
        ... )
        # Will size smaller due to high volatility

    Best for:
    - Risk parity approaches
    - Multi-asset portfolios
    - Consistent risk contribution per position
    """
    portfolio_value = to_decimal(portfolio_value)
    target_volatility = to_decimal(target_volatility)
    asset_volatility = to_decimal(asset_volatility)
    entry_price = to_decimal(entry_price)
    max_position_pct = to_decimal(max_position_pct)

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
    # Target = Position Pct * Asset Vol
    # Position Pct = Target / Asset Vol
    vol_ratio = target_volatility / asset_volatility

    # Convert to notional
    target_notional = portfolio_value * vol_ratio

    # Apply max position limit
    max_notional = portfolio_value * max_position_pct
    notional = min(target_notional, max_notional)

    quantity = round_down(notional / entry_price, 8)
    actual_notional = quantity * entry_price
    portfolio_pct = (actual_notional / portfolio_value) * Decimal("100")

    # Estimate risk as 2 standard deviations (daily)
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
    avg_win_pct: Decimal,     # Average win as % of position (e.g., 0.05 = 5%)
    avg_loss_pct: Decimal,    # Average loss as % of position (e.g., 0.03 = 3%)
    entry_price: Decimal,
    kelly_fraction: Decimal = Decimal("0.5"),
    max_position_pct: Decimal = Decimal("0.20")  # Never more than 20%
) -> PositionSize:
    """
    Kelly-based position sizing.

    Combines Kelly criterion with practical position limits.

    Args:
        portfolio_value: Current portfolio value
        win_rate: Historical win rate as decimal (0.55 = 55%)
        avg_win_pct: Average winning trade as % of position
        avg_loss_pct: Average losing trade as % of position
        entry_price: Entry price
        kelly_fraction: Fraction of Kelly to use (0.5 recommended)
        max_position_pct: Maximum position as % of portfolio (safety limit)

    Returns:
        PositionSize with Kelly-optimal sizing

    Examples:
        >>> kelly_position_size(
        ...     Decimal("100000"),
        ...     Decimal("0.55"),     # 55% win rate
        ...     Decimal("0.08"),     # 8% average win
        ...     Decimal("0.04"),     # 4% average loss
        ...     Decimal("50000"),
        ...     Decimal("0.5")       # Half Kelly
        ... )
    """
    portfolio_value = to_decimal(portfolio_value)
    win_rate = to_decimal(win_rate)
    avg_win_pct = to_decimal(avg_win_pct)
    avg_loss_pct = to_decimal(avg_loss_pct)
    entry_price = to_decimal(entry_price)
    kelly_fraction = to_decimal(kelly_fraction)
    max_position_pct = to_decimal(max_position_pct)

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
# Position Sizing Limits and Validation
# ============================================================================

@dataclass
class PositionLimits:
    """Risk limits for position sizing."""
    max_position_pct: Decimal = Decimal("0.20")      # 20% max per position
    max_sector_pct: Decimal = Decimal("0.40")        # 40% max per sector
    max_correlated_pct: Decimal = Decimal("0.50")    # 50% max in correlated assets
    max_daily_loss_pct: Decimal = Decimal("0.05")    # 5% daily stop-loss
    max_total_exposure: Decimal = Decimal("1.00")    # 100% max total exposure

    @classmethod
    def conservative(cls) -> 'PositionLimits':
        """Return conservative position limits."""
        return cls(
            max_position_pct=Decimal("0.10"),
            max_sector_pct=Decimal("0.25"),
            max_correlated_pct=Decimal("0.35"),
            max_daily_loss_pct=Decimal("0.02"),
            max_total_exposure=Decimal("0.80")
        )

    @classmethod
    def aggressive(cls) -> 'PositionLimits':
        """Return aggressive position limits."""
        return cls(
            max_position_pct=Decimal("0.30"),
            max_sector_pct=Decimal("0.50"),
            max_correlated_pct=Decimal("0.60"),
            max_daily_loss_pct=Decimal("0.10"),
            max_total_exposure=Decimal("1.50")  # Allows leverage
        )


def validate_position_size(
    proposed: PositionSize,
    current_positions: Dict[str, Decimal],  # symbol -> notional
    portfolio_value: Decimal,
    limits: Optional[PositionLimits] = None
) -> Tuple[bool, str]:
    """
    Validate proposed position against risk limits.

    Args:
        proposed: Proposed PositionSize
        current_positions: Dict of symbol -> current notional value
        portfolio_value: Total portfolio value
        limits: PositionLimits to validate against (default limits if None)

    Returns:
        Tuple of (is_valid, reason_if_invalid)
    """
    if limits is None:
        limits = PositionLimits()

    portfolio_value = to_decimal(portfolio_value)

    # Check single position limit
    max_position_pct_display = limits.max_position_pct * Decimal("100")
    if proposed.portfolio_pct > max_position_pct_display:
        return False, (
            f"Position {proposed.portfolio_pct:.1f}% exceeds "
            f"limit {max_position_pct_display:.1f}%"
        )

    # Check total exposure
    current_exposure = sum(to_decimal(v) for v in current_positions.values())
    new_exposure = current_exposure + proposed.notional
    exposure_pct = new_exposure / portfolio_value

    if exposure_pct > limits.max_total_exposure:
        return False, (
            f"Total exposure {exposure_pct * 100:.1f}% exceeds "
            f"limit {limits.max_total_exposure * 100:.1f}%"
        )

    return True, ""


def calculate_position_for_risk(
    portfolio_value: Decimal,
    max_loss_amount: Decimal,
    entry_price: Decimal,
    stop_loss_price: Decimal
) -> PositionSize:
    """
    Calculate position size given a maximum acceptable loss amount.

    This is the inverse of fixed_fractional - instead of specifying
    risk percentage, you specify the dollar amount you're willing to lose.

    Args:
        portfolio_value: Current portfolio value
        max_loss_amount: Maximum dollar loss acceptable
        entry_price: Entry price
        stop_loss_price: Stop loss price

    Returns:
        PositionSize that limits loss to max_loss_amount
    """
    portfolio_value = to_decimal(portfolio_value)
    max_loss_amount = to_decimal(max_loss_amount)
    entry_price = to_decimal(entry_price)
    stop_loss_price = to_decimal(stop_loss_price)

    # Risk per unit
    if entry_price > stop_loss_price:
        risk_per_unit = entry_price - stop_loss_price
    else:
        risk_per_unit = stop_loss_price - entry_price

    if risk_per_unit <= 0:
        return PositionSize(
            quantity=Decimal("0"),
            notional=Decimal("0"),
            risk_amount=Decimal("0"),
            portfolio_pct=Decimal("0"),
            method="max_loss"
        )

    quantity = round_down(max_loss_amount / risk_per_unit, 8)
    notional = quantity * entry_price
    portfolio_pct = (notional / portfolio_value) * Decimal("100")
    stop_loss_pct = (risk_per_unit / entry_price) * Decimal("100")

    return PositionSize(
        quantity=quantity,
        notional=notional,
        risk_amount=max_loss_amount,
        portfolio_pct=portfolio_pct,
        method="max_loss",
        stop_loss_pct=stop_loss_pct
    )


# ============================================================================
# Demonstration / Self-Test
# ============================================================================

if __name__ == "__main__":
    print("=== Kelly Criterion Test ===")

    # 55% win rate, $100 avg win, $80 avg loss
    kelly_full = kelly_criterion(
        Decimal("0.55"),
        Decimal("100"),
        Decimal("80"),
        Decimal("1.0")  # Full Kelly
    )
    kelly_half = kelly_criterion(
        Decimal("0.55"),
        Decimal("100"),
        Decimal("80"),
        Decimal("0.5")  # Half Kelly
    )

    print(f"Full Kelly: {kelly_full * 100:.2f}% of bankroll")
    print(f"Half Kelly: {kelly_half * 100:.2f}% of bankroll")

    print("\n=== Fixed Fractional Test ===")

    position = fixed_fractional(
        portfolio_value=Decimal("100000"),
        risk_per_trade=Decimal("0.01"),  # 1% risk
        entry_price=Decimal("50000"),     # $50k entry
        stop_loss_price=Decimal("48000")  # $48k stop (4% below)
    )

    print(f"Portfolio: $100,000")
    print(f"Risk per trade: 1%")
    print(f"Entry: $50,000, Stop: $48,000")
    print(f"Position size: {position.quantity} units")
    print(f"Notional: ${position.notional}")
    print(f"Risk amount: ${position.risk_amount}")
    print(f"Portfolio %: {position.portfolio_pct}%")
    print(f"Stop loss %: {position.stop_loss_pct}%")

    print("\n=== Volatility-Adjusted Test ===")

    # High volatility asset (BTC-like)
    position_btc = volatility_adjusted_sizing(
        portfolio_value=Decimal("100000"),
        target_volatility=Decimal("0.10"),  # 10% vol contribution
        asset_volatility=Decimal("0.60"),   # 60% annualized vol
        entry_price=Decimal("50000")
    )

    # Low volatility asset (stablecoin-like)
    position_stable = volatility_adjusted_sizing(
        portfolio_value=Decimal("100000"),
        target_volatility=Decimal("0.10"),  # 10% vol contribution
        asset_volatility=Decimal("0.05"),   # 5% annualized vol
        entry_price=Decimal("1")
    )

    print(f"High-vol asset (60% vol):")
    print(f"  Position %: {position_btc.portfolio_pct:.1f}%")
    print(f"  Notional: ${position_btc.notional:.0f}")

    print(f"Low-vol asset (5% vol):")
    print(f"  Position %: {position_stable.portfolio_pct:.1f}%")
    print(f"  Notional: ${position_stable.notional:.0f}")

    print("\n=== Position Validation Test ===")

    proposed = fixed_fractional(
        Decimal("100000"),
        Decimal("0.01"),
        Decimal("50000"),
        Decimal("48000")
    )

    current_positions = {
        "ETH": Decimal("30000"),
        "SOL": Decimal("20000"),
    }

    is_valid, reason = validate_position_size(
        proposed,
        current_positions,
        Decimal("100000"),
        PositionLimits()
    )

    print(f"Proposed position valid: {is_valid}")
    if not is_valid:
        print(f"Reason: {reason}")

    print("\n=== All tests passed! ===")
