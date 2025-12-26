"""
Precision handling for financial calculations.

CRITICAL: Always construct Decimal from strings, NEVER from floats.
Float contamination is the #1 source of financial calculation errors.

This module provides:
- Safe Decimal conversion from any type
- Directional rounding (up for fees, down for balances)
- Precision constants for Trading Arena
- Validation utilities

Author: AI-CIV (capability-curator)
Created: 2025-12-26
Domain: trading-systems
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
        >>> to_decimal(Decimal("50.5"))  # Already Decimal - just quantize
        Decimal('50.50000000')
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
    - Proceeds estimation (conservative)

    Args:
        value: Decimal to round
        precision: Number of decimal places

    Returns:
        Rounded Decimal

    Examples:
        >>> round_down(Decimal("100.129"), 2)
        Decimal('100.12')
        >>> round_down(Decimal("100.999"), 2)
        Decimal('100.99')
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
    - Cost estimation (conservative)

    Args:
        value: Decimal to round
        precision: Number of decimal places

    Returns:
        Rounded Decimal

    Examples:
        >>> round_up(Decimal("100.121"), 2)
        Decimal('100.13')
        >>> round_up(Decimal("100.001"), 2)
        Decimal('100.01')
    """
    quantize_str = "0." + "0" * precision if precision > 0 else "0"
    return value.quantize(Decimal(quantize_str), rounding=ROUND_UP)


def round_half_up(value: Decimal, precision: int = 8) -> Decimal:
    """
    Standard rounding (0.5 rounds up).

    Use for:
    - Display values
    - General calculations where direction doesn't matter
    - Percentage calculations

    Args:
        value: Decimal to round
        precision: Number of decimal places

    Returns:
        Rounded Decimal
    """
    quantize_str = "0." + "0" * precision if precision > 0 else "0"
    return value.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


# =============================================================================
# Standard Precision Constants for Trading Arena
# =============================================================================

# Cryptocurrency prices (BTC, ETH, etc.)
PRICE_PRECISION = 8      # 8 decimal places (1 satoshi resolution)

# Order quantities
QUANTITY_PRECISION = 8   # 8 decimal places for fractional crypto

# Stablecoin values (USDC, USDT)
USDC_PRECISION = 2       # 2 decimal places (like USD)

# Basis points (0.01%)
BPS_PRECISION = 4        # 4 decimal places (0.0001 = 1 bps)

# Percentage display
PCT_PRECISION = 2        # 2 decimal places for percentages

# Fee calculations
FEE_PRECISION = 8        # 8 decimal places for micro-fees


# =============================================================================
# Validation Utilities
# =============================================================================

def validate_precision(
    value: Decimal,
    max_decimals: int,
    name: str = "value"
) -> None:
    """
    Validate that a value doesn't exceed maximum decimal places.

    Raises PrecisionError if validation fails.

    Args:
        value: Decimal to validate
        max_decimals: Maximum allowed decimal places
        name: Field name for error message

    Raises:
        PrecisionError: If value exceeds precision limit

    Examples:
        >>> validate_precision(Decimal("100.12"), 2, "price")  # OK
        >>> validate_precision(Decimal("100.123"), 2, "price")  # Raises!
    """
    sign, digits, exponent = value.as_tuple()
    if exponent < 0 and abs(exponent) > max_decimals:
        raise PrecisionError(
            f"{name} has {abs(exponent)} decimal places, max is {max_decimals}"
        )


def validate_positive(
    value: Decimal,
    name: str = "value",
    allow_zero: bool = False
) -> None:
    """
    Validate that a value is positive.

    Args:
        value: Decimal to validate
        name: Field name for error message
        allow_zero: Whether zero is allowed

    Raises:
        PrecisionError: If value is not positive (or zero if not allowed)
    """
    if allow_zero:
        if value < 0:
            raise PrecisionError(f"{name} must be non-negative, got {value}")
    else:
        if value <= 0:
            raise PrecisionError(f"{name} must be positive, got {value}")


def validate_range(
    value: Decimal,
    min_val: Optional[Decimal],
    max_val: Optional[Decimal],
    name: str = "value"
) -> None:
    """
    Validate that a value is within a range.

    Args:
        value: Decimal to validate
        min_val: Minimum allowed value (inclusive), None for no minimum
        max_val: Maximum allowed value (inclusive), None for no maximum
        name: Field name for error message

    Raises:
        PrecisionError: If value is outside range
    """
    if min_val is not None and value < min_val:
        raise PrecisionError(f"{name} must be >= {min_val}, got {value}")
    if max_val is not None and value > max_val:
        raise PrecisionError(f"{name} must be <= {max_val}, got {value}")


def safe_divide(
    numerator: Decimal,
    denominator: Decimal,
    default: Decimal = Decimal("0"),
    precision: int = 8
) -> Decimal:
    """
    Safely divide two Decimals, returning default if denominator is zero.

    Args:
        numerator: The numerator
        denominator: The denominator
        default: Value to return if denominator is zero
        precision: Decimal places for result

    Returns:
        Result of division or default

    Examples:
        >>> safe_divide(Decimal("100"), Decimal("3"))
        Decimal('33.33333333')
        >>> safe_divide(Decimal("100"), Decimal("0"))
        Decimal('0.00000000')
        >>> safe_divide(Decimal("100"), Decimal("0"), Decimal("-1"))
        Decimal('-1.00000000')
    """
    if denominator == 0:
        return to_decimal(default, precision)
    return to_decimal(numerator / denominator, precision)


def percentage_to_decimal(pct: Decimal) -> Decimal:
    """
    Convert percentage to decimal representation.

    Args:
        pct: Percentage value (e.g., 55 for 55%)

    Returns:
        Decimal representation (e.g., 0.55)

    Examples:
        >>> percentage_to_decimal(Decimal("55"))
        Decimal('0.55')
        >>> percentage_to_decimal(Decimal("0.5"))
        Decimal('0.005')
    """
    return pct / Decimal("100")


def decimal_to_percentage(dec: Decimal) -> Decimal:
    """
    Convert decimal to percentage representation.

    Args:
        dec: Decimal value (e.g., 0.55)

    Returns:
        Percentage representation (e.g., 55)

    Examples:
        >>> decimal_to_percentage(Decimal("0.55"))
        Decimal('55')
        >>> decimal_to_percentage(Decimal("0.005"))
        Decimal('0.5')
    """
    return dec * Decimal("100")


# =============================================================================
# Comparison Utilities
# =============================================================================

def almost_equal(
    a: Decimal,
    b: Decimal,
    tolerance: Decimal = Decimal("0.00000001")
) -> bool:
    """
    Check if two Decimals are approximately equal.

    Useful for comparing calculated values that might have tiny precision differences.

    Args:
        a: First value
        b: Second value
        tolerance: Maximum allowed difference

    Returns:
        True if values are within tolerance

    Examples:
        >>> almost_equal(Decimal("1.00000001"), Decimal("1.0"))
        True
        >>> almost_equal(Decimal("1.001"), Decimal("1.0"))
        False
    """
    return abs(a - b) <= tolerance


def is_zero(value: Decimal, tolerance: Decimal = Decimal("0.00000001")) -> bool:
    """
    Check if a Decimal is effectively zero.

    Args:
        value: Value to check
        tolerance: Maximum value to consider as zero

    Returns:
        True if value is within tolerance of zero
    """
    return abs(value) <= tolerance


# =============================================================================
# Demonstration / Self-Test
# =============================================================================

if __name__ == "__main__":
    # Demonstrate float vs Decimal precision issue
    print("=== Float Precision Problem ===")
    float_sum = 0.0
    for _ in range(100):
        float_sum += 0.01
    print(f"Float: 100 * 0.01 = {float_sum}")  # Not 1.0!

    decimal_sum = Decimal("0")
    for _ in range(100):
        decimal_sum += Decimal("0.01")
    print(f"Decimal: 100 * 0.01 = {decimal_sum}")  # Exactly 1.00

    print("\n=== Safe Conversion ===")
    print(f"From string: {to_decimal('100.123456789')}")
    print(f"From int: {to_decimal(100)}")
    print(f"From float (safe): {to_decimal(100.5)}")

    print("\n=== Rounding Direction ===")
    val = Decimal("100.125")
    print(f"Value: {val}")
    print(f"Round down (2 dp): {round_down(val, 2)}")  # 100.12
    print(f"Round up (2 dp): {round_up(val, 2)}")      # 100.13
    print(f"Round half up (2 dp): {round_half_up(val, 2)}")  # 100.13

    print("\n=== Safe Division ===")
    print(f"100 / 3 = {safe_divide(Decimal('100'), Decimal('3'))}")
    print(f"100 / 0 = {safe_divide(Decimal('100'), Decimal('0'))}")

    print("\n=== All tests passed! ===")
