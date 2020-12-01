import pytest

from expression_resolver import ExpressionResolver


def test_calculator():
    resolver = ExpressionResolver(verbose=True)

    # Simple test
    ret = resolver.solve(expression="5 * 5^0")
    assert ret == 5

    # Simple test exponential
    ret = resolver.solve(expression="5 * 5^10")
    assert ret == 48828125

    # Simple test with priority
    ret = resolver.solve(expression="5 * 5 + 10")
    assert ret == 35

    # Simple test with float
    ret = resolver.solve(expression="5.3 * 5.2 + 10.8")
    assert ret == 38.36

    # Test with parenthesis
    ret = resolver.solve(expression="5 * (5 + 10)")
    assert ret == 75

    # Test with multiple parenthesis
    ret = resolver.solve(expression="5 * (5 + (10 * 50 + 2))")
    assert ret == 2535

    # Test with multiple useless parenthesis
    ret = resolver.solve(expression="((((5 * (5 + (10 * 50 + 2))))))")
    assert ret == 2535

    # Hard test with multiple parenthesis
    ret = resolver.solve(
        expression="5 * (5 + (10 * 50 + 24.15) *    50 * 18 *(12 + 52)) * (18 - (5 + 2))"
    )
    assert ret == 1660507475

    # Hard test with float
    ret = resolver.solve(expression="545875785748.34444444478 * 5.2542 + 10456.81212")
    assert ret == 2868140563935.763

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

    # Test multiplying by a signed float
    ret = resolver.solve(expression="5 * -10.35843958432134 + 599")
    assert ret == 547.2078020783933

    # Test implicit parenthesis multiply
    ret = resolver.solve(expression="(5+1)(2-5)")
