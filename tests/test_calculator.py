import pytest

from ..computor import ExpressionResolver


def test_calculator():
    resolver = ExpressionResolver()

    # Simple test
    ret = resolver.solve(expression="5 * 5^0")
    assert ret == 5

    # Simple test exponential
    ret = resolver.solve(expression="5 * 5^10")
    assert ret == 48828125

    # Simple test with priority
    ret = resolver.solve(expression="5 * 5 + 10")
    assert ret == 35

    # Test with parenthesis
    ret = resolver.solve(expression="5 * (5 + 10)")
    assert ret == 75

    # Test with multiple parenthesis
    ret = resolver.solve(expression="5 * (5 + (10 * 50 + 2))")
    assert ret == 2535

    # Hard test with multiple parenthesis
    ret = resolver.solve(
        expression="5 * (5 + (10 * 50 + 24.15) *    50 * 18 *(12 + 52)) * (18 - (5 + 2))"
    )
    assert ret == 1660507475

    # Test with wrong parenthesis number
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 * (5 + (10 * 50 + 2)")
    assert str(e.value) == "Problem with parenthesis."

    # Test with wrong parenthesis number
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 * (5 + (10 * 50 + (2))")
    assert str(e.value) == "Problem with parenthesis."

    # Test with right parenthesis number but not good open/close order
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 * (5)10 * 50 + )2()(")
    assert str(e.value) == "Closing parenthesis with no opened one."

    # Test with right parenthesis number but not good open/close order
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 + (5 + 10) + 2)(15*2")
    assert str(e.value) == "Closing parenthesis with no opened one."

    # Implicit multiplication with open parenthesis
    ret = resolver.solve(expression="25(5 + 2)")
    assert ret == 175

    # Implicit multiplication with closing parenthesis
    ret = resolver.solve(expression="(5 + 2)25")
    assert ret == 175

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * -10 + 599")
    assert ret == 549

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * +10")
    assert ret == 50

    # Test multiplying by a signed number in parenthesis
    ret = resolver.solve(expression="5 * (+10)")
    assert ret == 50

    # Test multiplying by a signed number in parenthesis
    ret = resolver.solve(expression="(+10)10")
    assert ret == 100

    # Test substract by a signed number in parenthesis
    ret = resolver.solve(expression="(-10)-10")
    assert ret == -20

    # Test substract by a signed number in parenthesis
    ret = resolver.solve(expression="(-10)(-10)")
    assert ret == 100

    # Test implicit parenthesis multiply
    ret = resolver.solve(expression="(5+1)(2-5)")
