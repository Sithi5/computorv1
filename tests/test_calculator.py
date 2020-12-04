import pytest

from expression_resolver import ExpressionResolver


def test_calculator():
    resolver = ExpressionResolver(verbose=False)

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

    # Test sign before first number
    ret = resolver.solve(expression="-42-2")
    assert ret == -44


def test_calculator_with_one_var():
    resolver = ExpressionResolver(verbose=True)

    # # Test calc with var, only one var alone
    # ret = resolver.solve(expression="thisisavar")
    # assert ret == "THISISAVAR"

    # # Test calc with var, one var with simple addition
    # ret = resolver.solve(expression="thisisavar + 5")
    # assert ret == "5.0+THISISAVAR"

    # # Test calc with var, one var with simple addition
    # ret = resolver.solve(expression="5 + thisisavar + 5")
    # assert ret == "10.0+THISISAVAR"

    # # Test calc with var, one var with more complex addition
    # ret = resolver.solve(expression="5 + thisisavar + 5 (-10 +(+5))")
    # assert ret == "-20.0+THISISAVAR"

    # # Test calc with var, one var with multiplication
    # ret = resolver.solve(expression="5 * thisisavar")
    # assert ret == "5.0*THISISAVAR"

    # # Test calc with var, one var with multiplication
    # ret = resolver.solve(expression="(5 * 2) * thisisavar")
    # assert ret == "10.0*THISISAVAR"

    # # Test calc with var, one var with multiplication
    # ret = resolver.solve(expression="(5 * 2) * thisisavar * 2")
    # assert ret == "20.0*THISISAVAR"

    # # Test calc with var, one var with multiplication and additions
    # ret = resolver.solve(expression="+ 2 - 5 + (5 * 2) * thisisavar * 2 - 500")
    # assert ret == "-503.0+20.0*THISISAVAR"

    # # Test calc with var, implicit mult
    # ret = resolver.solve(expression="-5 - 2thisisavar2")
    # assert ret == "-5.0-4.0*THISISAVAR"

    # # Test calc with var, implicit mult
    # ret = resolver.solve(expression="-5 - 2thisisavar(2(2+5))")
    # assert ret == "-5.0-28.0*THISISAVAR"

    # Test calc with var, var in simple parenthesis
    ret = resolver.solve(expression="-5 - (2thisisavar(2(2+5)) * -1)")
    assert ret == "-28.0*THISISAVAR"


def test_calculator_wrong_args():
    resolver = ExpressionResolver(verbose=False)

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
