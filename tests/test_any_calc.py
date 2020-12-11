import pytest

from expression_resolver import ExpressionResolver
from calculator import _Calculator


def test_any_calc():
    resolver = ExpressionResolver(verbose=False)
    calculator = _Calculator()

    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression=" (5 + 2y)(2 - (2y * 3y))")
    assert str(e.value) == "Var cannot be inside a parenthesis for the moment."

    ret = resolver.solve(expression="y[5 + 2](2 - {2 * -3.54]]")
    assert ret == "63.56*Y"

    ret = resolver.solve(expression="5y/y")
    assert ret == "5.0"

    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression=" -5 - 4 * X + X^2= X^2 + x^5")
    assert (
        str(e.value)
        == "The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
    )
