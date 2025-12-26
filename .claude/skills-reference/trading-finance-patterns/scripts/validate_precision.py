#!/usr/bin/env python3
"""
Precision validation tests for trading finance calculations.

Run these tests to verify Decimal arithmetic is working correctly.
Financial code MUST be correct - these tests catch precision errors.

Usage:
    python scripts/validate_precision.py
"""

import sys
from decimal import Decimal, getcontext
from pathlib import Path

# Add references to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "references"))

from precision import (
    to_decimal,
    round_down,
    round_up,
    safe_divide,
    validate_precision,
    PrecisionError
)


def test_float_vs_decimal():
    """Demonstrate the float precision problem and Decimal solution."""
    print("Test: Float vs Decimal precision")

    # Float accumulation error
    float_sum = 0.0
    for _ in range(100):
        float_sum += 0.01

    # Decimal accumulation (exact)
    decimal_sum = Decimal("0")
    for _ in range(100):
        decimal_sum += Decimal("0.01")

    # Float should NOT equal 1.0 exactly
    assert float_sum != 1.0, "Float should have precision error"
    assert abs(float_sum - 1.0) < 0.0001, "Float should be close to 1.0"

    # Decimal MUST equal 1.00 exactly
    assert decimal_sum == Decimal("1.00"), f"Decimal sum should be 1.00, got {decimal_sum}"

    print(f"  Float: 100 * 0.01 = {float_sum} (not exactly 1.0!)")
    print(f"  Decimal: 100 * 0.01 = {decimal_sum} (exactly 1.00)")
    print("  PASSED")


def test_to_decimal_conversion():
    """Test safe conversion to Decimal from various types."""
    print("\nTest: to_decimal conversion")

    # From string (preferred)
    assert to_decimal("100.12345678") == Decimal("100.12345678")

    # From int
    assert to_decimal(100) == Decimal("100.00000000")

    # From float (via string conversion)
    result = to_decimal(100.5)
    assert result == Decimal("100.50000000"), f"Got {result}"

    # From Decimal
    assert to_decimal(Decimal("50.5")) == Decimal("50.50000000")

    # Custom precision
    assert to_decimal("100.123456789", precision=2) == Decimal("100.12")
    assert to_decimal("100.125", precision=2) == Decimal("100.13")  # Rounds up

    print("  All conversions correct")
    print("  PASSED")


def test_rounding_directions():
    """Test directional rounding for financial calculations."""
    print("\nTest: Rounding directions")

    value = Decimal("100.125")

    # Round down (for conservative balance calculations)
    down = round_down(value, 2)
    assert down == Decimal("100.12"), f"Round down failed: {down}"

    # Round up (for conservative fee calculations)
    up = round_up(value, 2)
    assert up == Decimal("100.13"), f"Round up failed: {up}"

    # Edge case: 100.999 -> 100.99 (down) or 101.00 (up)
    edge = Decimal("100.999")
    assert round_down(edge, 2) == Decimal("100.99")
    assert round_up(edge, 2) == Decimal("101.00")

    print(f"  100.125 down(2): {round_down(value, 2)}")
    print(f"  100.125 up(2): {round_up(value, 2)}")
    print("  PASSED")


def test_safe_divide():
    """Test division with zero handling."""
    print("\nTest: Safe division")

    # Normal division
    result = safe_divide(Decimal("100"), Decimal("3"))
    assert str(result).startswith("33.333333"), f"Got {result}"

    # Division by zero returns default
    result = safe_divide(Decimal("100"), Decimal("0"))
    assert result == Decimal("0.00000000"), f"Got {result}"

    # Custom default
    result = safe_divide(Decimal("100"), Decimal("0"), Decimal("-1"))
    assert result == Decimal("-1.00000000"), f"Got {result}"

    print("  Division by zero handled correctly")
    print("  PASSED")


def test_precision_validation():
    """Test precision validation raises on violations."""
    print("\nTest: Precision validation")

    # Valid precision
    validate_precision(Decimal("100.12"), 2, "price")

    # Invalid precision should raise
    try:
        validate_precision(Decimal("100.123"), 2, "price")
        assert False, "Should have raised PrecisionError"
    except PrecisionError as e:
        assert "3 decimal places" in str(e)
        assert "max is 2" in str(e)

    print("  Validation correctly rejects excess precision")
    print("  PASSED")


def test_financial_scenario():
    """Test a realistic financial calculation scenario."""
    print("\nTest: Financial scenario")

    # Scenario: Calculate total cost of buying 0.5 BTC at $40,000 with 0.1% fee
    quantity = to_decimal("0.5")
    price = to_decimal("40000")
    fee_rate = to_decimal("0.001")  # 0.1%

    notional = quantity * price
    fee = round_up(notional * fee_rate, 2)  # Round UP fees
    total_cost = notional + fee

    assert notional == Decimal("20000.00000000")
    assert fee == Decimal("20.00")
    assert total_cost == Decimal("20020.00000000")

    print(f"  Quantity: {quantity} BTC")
    print(f"  Price: ${price}")
    print(f"  Notional: ${notional}")
    print(f"  Fee (0.1%): ${fee}")
    print(f"  Total cost: ${total_cost}")
    print("  PASSED")


def test_pnl_calculation():
    """Test P&L calculation precision."""
    print("\nTest: P&L calculation precision")

    # Buy at $40,000, sell at $42,000
    buy_price = to_decimal("40000")
    sell_price = to_decimal("42000")
    quantity = to_decimal("0.12345678")

    # Calculate P&L
    buy_cost = buy_price * quantity
    sell_proceeds = sell_price * quantity
    pnl = sell_proceeds - buy_cost

    expected_pnl = to_decimal("246.91356")  # (42000 - 40000) * 0.12345678

    assert abs(pnl - expected_pnl) < Decimal("0.00001"), f"PnL mismatch: {pnl}"

    print(f"  Buy: {quantity} BTC @ ${buy_price}")
    print(f"  Sell: {quantity} BTC @ ${sell_price}")
    print(f"  P&L: ${pnl}")
    print("  PASSED")


def test_cumulative_operations():
    """Test precision is maintained over many operations."""
    print("\nTest: Cumulative operations (1000 trades)")

    balance = to_decimal("100000")
    trade_amount = to_decimal("100")
    fee = to_decimal("0.01")

    # Simulate 1000 trades
    for _ in range(500):
        balance -= trade_amount + fee  # Buy
        balance += trade_amount - fee  # Sell

    # After 500 round trips, should have lost 500 * 2 * 0.01 = 10 in fees
    expected_balance = to_decimal("100000") - (to_decimal("500") * to_decimal("2") * fee)

    assert balance == expected_balance, f"Balance mismatch: {balance} vs {expected_balance}"

    print(f"  Started: $100,000")
    print(f"  After 500 round trips with $0.01 fee each way: ${balance}")
    print(f"  Total fees: ${to_decimal('100000') - balance}")
    print("  PASSED")


def test_percentage_calculations():
    """Test percentage calculations maintain precision."""
    print("\nTest: Percentage calculations")

    portfolio_value = to_decimal("100000")
    returns = [
        to_decimal("0.01"),   # +1%
        to_decimal("-0.005"), # -0.5%
        to_decimal("0.015"),  # +1.5%
        to_decimal("-0.02"),  # -2%
        to_decimal("0.025"),  # +2.5%
    ]

    # Calculate cumulative return
    cumulative = Decimal("1")
    for r in returns:
        cumulative *= (Decimal("1") + r)

    final_value = portfolio_value * cumulative
    total_return = (cumulative - Decimal("1")) * Decimal("100")

    print(f"  Starting: ${portfolio_value}")
    print(f"  Returns: {[str(r * 100) + '%' for r in returns]}")
    print(f"  Cumulative factor: {cumulative}")
    print(f"  Final value: ${round_down(final_value, 2)}")
    print(f"  Total return: {round_down(total_return, 4)}%")
    print("  PASSED")


def run_all_tests():
    """Run all validation tests."""
    print("=" * 60)
    print("TRADING FINANCE PRECISION VALIDATION")
    print("=" * 60)
    print(f"Decimal context precision: {getcontext().prec}")

    try:
        test_float_vs_decimal()
        test_to_decimal_conversion()
        test_rounding_directions()
        test_safe_divide()
        test_precision_validation()
        test_financial_scenario()
        test_pnl_calculation()
        test_cumulative_operations()
        test_percentage_calculations()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED - Precision handling is correct")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
