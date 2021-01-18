import pytest

from expression_resolver import ExpressionResolver
from exception import NothingToDoError
from utils import my_round


def test_calculator():
    resolver = ExpressionResolver(verbose=False)

    # Simple test
    ret = resolver.solve(expression="5 * 5^0")
    assert ret == "5.0"

    # Simple test exponential
    ret = resolver.solve(expression="5 * 5^10")
    assert ret == "48828125.0"

    # Simple test with priority
    ret = resolver.solve(expression="5 * 5 + 10")
    assert ret == "35.0"

    # Simple test with float
    ret = resolver.solve(expression="5.3 * 5.2 + 10.8")
    assert ret == "38.36"

    # Test with parenthesis
    ret = resolver.solve(expression="5 * (5 + 10)")
    assert ret == "75.0"

    # Test with multiple parenthesis
    ret = resolver.solve(expression="5 * (5 + (10 * 50 + 2))")
    assert ret == "2535.0"

    # Test with multiple useless parenthesis
    ret = resolver.solve(expression="((((5 * (5 + (10 * 50 + 2))))))")
    assert ret == "2535.0"

    # Hard test with multiple parenthesis
    ret = resolver.solve(
        expression="5 * (5 + (10 * 50 + 24.15) *    50 * 18 *(12 + 52)) * (18 - (5 + 2))"
    )
    assert ret == "1660507475.0"

    # Hard test with float
    ret = resolver.solve(expression="545875785748.34444444478 * 5.2542 + 10456.81212")
    assert my_round(float(ret), 2) == my_round(2868140563935.763, 2)

    # Implicit multiplication with open parenthesis
    ret = resolver.solve(expression="25(5 + 2)")
    assert ret == "175.0"

    # Implicit multiplication with closing parenthesis
    ret = resolver.solve(expression="(5 + 2)25")
    assert ret == "175.0"

    # Test different parenthesis
    ret = resolver.solve(expression="(5 + 2]25")
    assert ret == "175.0"

    # Test different parenthesis
    ret = resolver.solve(expression="[5 + 2]25")
    assert ret == "175.0"

    # Test different parenthesis
    ret = resolver.solve(expression="[5 + 2}25")
    assert ret == "175.0"

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * -10 + 599")
    assert ret == "549.0"

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * +10")
    assert ret == "50.0"

    # Test multiplying by a signed number in parenthesis
    ret = resolver.solve(expression="5 * (+10)")
    assert ret == "50.0"

    # Test multiplying by a signed number in parenthesis
    ret = resolver.solve(expression="(+10)10")
    assert ret == "100.0"

    # Test substract by a signed number in parenthesis
    ret = resolver.solve(expression="(-10)-10")
    assert ret == "-20.0"

    # Test substract by a signed number in parenthesis
    ret = resolver.solve(expression="(-10)(-10)")
    assert ret == "100.0"

    # Test multiplying by a signed float
    ret = resolver.solve(expression="5 * -10.35843958432134 + 599")
    assert my_round(float(ret), 2) == my_round(547.2078020783933, 2)

    # Test sign before first number
    ret = resolver.solve(expression="-42-2")
    assert ret == "-44.0"

    # Test one var with parenthesis in calculator
    ret = resolver.solve(expression="5 * x(5 + 10)")
    assert ret == "75.0*X"


def test_calculator_with_one_var():
    resolver = ExpressionResolver(verbose=False)

    # Test calc with var, only one var alone, should raise NothingToDoError
    with pytest.raises(NothingToDoError) as e:
        resolver.solve(expression="thisisavar")
    assert str(e.value) == "There is no operators or sign in the expression. Nothing to do here."

    # Test calc with var, one var with simple addition
    ret = resolver.solve(expression="thisisavar + 5")
    assert ret == "5.0+THISISAVAR"

    # Test calc with var, one var with simple addition
    ret = resolver.solve(expression="5 + thisisavar + 5")
    assert ret == "10.0+THISISAVAR"

    # Test calc with var, one var with more complex addition
    ret = resolver.solve(expression="5 + thisisavar + 5 (-10 +(+5))")
    assert ret == "-20.0+THISISAVAR"

    # Test calc with var, one var with multiplication
    ret = resolver.solve(expression="5 * thisisavar")
    assert ret == "5.0*THISISAVAR"

    # Test calc with var, one var with multiplication
    ret = resolver.solve(expression="(5 * 2) * thisisavar")
    assert ret == "10.0*THISISAVAR"

    # Test calc with var, one var with multiplication
    ret = resolver.solve(expression="(5 * 2) * thisisavar * 2")
    assert ret == "20.0*THISISAVAR"

    # Test calc with var, one var with multiplication and additions
    ret = resolver.solve(expression="+ 2 - 5 + (5 * 2) * thisisavar * 2 - 500")
    assert ret == "-503.0+20.0*THISISAVAR"

    # Test calc with var, implicit mult
    ret = resolver.solve(expression="-5 - 2thisisavar2")
    assert ret == "-5.0-4.0*THISISAVAR"

    # Test calc with var, implicit mult
    ret = resolver.solve(expression="-5 - 2thisisavar(2(2+5))")
    assert ret == "-5.0-28.0*THISISAVAR"

    # Test calc with var, addition between var
    ret = resolver.solve(expression="x + x")
    assert ret == "2.0X"

    # Test calc with var
    ret = resolver.solve(expression="1 * x")
    assert ret == "X"

    # Test calc with var
    ret = resolver.solve(expression="5 * x")
    assert ret == "5.0*X"

    # Test calc with var
    ret = resolver.solve(expression="-1 * x")
    assert ret == "-X"

    # Test calc with var, addition between var
    ret = resolver.solve(expression="-5 - x + x * -1")
    assert ret == "-5.0-2.0X"

    # Test calc with var, sub between var
    ret = resolver.solve(expression="x - x")
    assert ret == "0.0"

    # Test calc with var, sub between var
    ret = resolver.solve(expression="54x - x(-2)")
    assert ret == "56.0X"

    # Test calc with var, multiplication between var
    ret = resolver.solve(expression="x * x")
    assert ret == "X^2.0"

    # Test calc with var, multiplication between var
    ret = resolver.solve(expression="x * 5x")
    assert ret == "5.0*X^2.0"

    # Test calc with var, multiplication between var
    ret = resolver.solve(expression="x * x * x + (5 * 2)")
    assert ret == "10.0+X^3.0"

    # Test calc with var, dividing var
    ret = resolver.solve(expression="x / 50 * x + (5 * 2)")
    assert ret == "10.0+0.02*X^2.0"

    # Test calc with var, dividing var by another var
    ret = resolver.solve(expression="x / 5 / x + (5 * 2)")
    assert ret == "10.2"

    # Test calc with var, dividing var by another var
    ret = resolver.solve(expression="2x / 5 / x + (5 * 2)")
    assert ret == "10.4"

    # Test calc with var, dividing var by another var
    ret = resolver.solve(expression="2x^5 / 5 / x   + (5 * 2)")
    assert ret == "10.0+0.4*X^4.0"

    # Test calc with var, dividing var by another var
    ret = resolver.solve(expression="2x^5 / 5 / x *x   + (5 * 2)")
    assert ret == "10.0+0.4*X^5.0"

    # Test calc with var, dividing var by another var
    ret = resolver.solve(expression="50x/x")
    assert ret == "50.0"

    # Test calc with var, power var
    ret = resolver.solve(expression="50x^2")
    assert ret == "50.0*X^2.0"

    # Test calc with var, power var
    ret = resolver.solve(expression="50x^(2+5)")
    assert ret == "50.0*X^7.0"


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

    # Test two var in calculator
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 * x(5 + 10) * y")
    assert str(e.value) == "Calculator does not accept more than 1 var."

    # Test wrong operation for vars
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="5 * x% 2")
    assert str(e.value) == "This type of operation with vars is not accepted for the moment."

    # Test wrong operation for vars
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="5 * x% x")
    assert str(e.value) == "This type of operation with vars is not accepted for the moment."

    # Test calc with var, var in simple parenthesis
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="-5 - (2thisisavar(2(2+5)) * -1)")
    assert str(e.value) == "Var cannot be inside a parenthesis for the moment."

    # Test calc with var, dividing number by a var
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="50 / x * x + (5 * 2)")
    assert str(e.value) == "Cannot divide a number by a var for the moment."

    # Test calc with var, power var by var
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="50x^X")
    assert str(e.value) == "Cannot power a var by a var for the moment."

    # Test calc with var, power number by var
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="50^X")
    assert str(e.value) == "Cannot power a number by a var for the moment."
