import pytest

from computor import ExpressionResolver


def test_expression_resolver():
    resolver = ExpressionResolver()

    # Test sign before
    ret = resolver.solve(expression="+X = Hello world")

    # Test sign before
    ret = resolver.solve(expression="-X = Hello world")

    # Test addition with sign before var
    ret = resolver.solve(expression="X -Y = X")

    # lot of sign
    ret = resolver.solve(expression="4-+-2 ------+-----++++++ X^0 = 0")

    # lot of sign
    ret = resolver.solve(expression="4-+-2 ------+-----++++++ X^+-+++-0 = 0")


def test_equations():
    resolver = ExpressionResolver()

    # Polynomial degree 2
    ret = resolver.solve(expression="5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")

    # Polynomial degree 1
    ret = resolver.solve(expression="5 * X^0 + 4 * X^1 = 4 * X^0")

    # Polynomial degree 3
    ret = resolver.solve(expression="8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")

    # Polynomial degree 1, result should be N
    ret = resolver.solve(expression="42 * X^0 = 42 * X^0")

    # Test big name var
    ret = resolver.solve(expression="Hello world*10+1245 = Hello world")


def test_calculator():
    resolver = ExpressionResolver()

    # Simple test
    ret = resolver.solve(expression="5 * 5^0")
    assert ret == 5

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
        ret = resolver.solve(expression="5 * (5 + )10 * 50 + )2()(")
    assert str(e.value) == "Closing parenthesis with no opened one."

    # Test with right parenthesis number but not good open/close order
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 + (5 + 10) + 2)(15*2")
    assert str(e.value) == "Closing parenthesis with no opened one."

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * -10")
    assert ret == -50

    # Test multiplying by a signed number
    ret = resolver.solve(expression="5 * +10")
    assert ret == 50


def test_wrong_args():
    resolver = ExpressionResolver()

    # Wrong args
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="6&7-2=5")
    assert str(e.value) == "This is not an expression or some of the operators are not reconized."

    # Sign without value after
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="4^0-")
    assert str(e.value) == "Operators or sign must be followed by a value or a variable."

    # Operator wrong syntax
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="42//5")
    assert (
        str(e.value) == "Operators must be followed by a value or a variable, not another operator."
    )

    # Tests var in calculator
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="X+18+ 5")
    assert str(e.value) == "Calculator does not support variables."

    # More than one = in the expression
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="42 * X = 42 * Y = 42 * Z")
        out, err = capsys.readouterr()
    assert str(e.value) == "More than one comparison is not supported for the moment."

    # lot of sign and operator between
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="4X^+-+^++-0 = 0")
    assert (
        str(e.value) == "Operators must be followed by a value or a variable, not another operator."
    )

    # multiple comma in one number
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="450.25.45 + 12")
    assert str(e.value) == "Some numbers are not well formated (Comma error)."

    # wrong use of comma
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="450. + 12")
    assert str(e.value) == "Some numbers are not well formated (Comma error)."

    # wrong use of comma
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression=".45 + 12")
    assert str(e.value) == "Some numbers are not well formated (Comma error)."

    # Implicit multiplication with parenthesis
    with pytest.raises(Exception) as e:
        ret = resolver.solve(expression="25(5 + 2)")
    assert (
        str(e.value)
        == "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
    )
