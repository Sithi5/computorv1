# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_equations.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:30 by mabouce           #+#    #+#              #
#    Updated: 2021/01/18 17:51:39 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pytest

import math

from expression_resolver import ExpressionResolver


def test_equation_subject():
    resolver = ExpressionResolver(verbose=False)

    ret = resolver.solve(expression="5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
    assert ret == ["-0.475131", "0.905239"]

    ret = resolver.solve(expression="5 * X^0 + 4 * X^1 = 4 * X^0")
    assert ret == "-0.25"

    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
    assert (
        str(e.value)
        == "The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
    )

    ret = resolver.solve(expression="5 + 4 * X + X^2= X^2")


def test_equation_degree_one():
    resolver = ExpressionResolver(verbose=False)

    ret = resolver.solve(expression="5 * X^0 + 4 * X^1 = 41 * X^0")
    assert ret == "9.0"

    ret = resolver.solve(expression="-51516544 * X^0 + 4241.1 * X^1 + 1213545 = ---41 * X^0 + -X^1")
    assert ret == "11858.032106739585"

    ret = resolver.solve(expression="X ^1 = X ^ 1")
    assert ret == "X can be any real number."

    ret = resolver.solve(expression="X = X")
    assert ret == "X can be any real number."

    ret = resolver.solve(expression="X^0 = X^0")
    assert ret == "X can be any real number."


def test_equation_degree_two():
    resolver = ExpressionResolver(verbose=False)

    ret = resolver.solve(expression="x^2+x-2 = 0")
    assert ret == ["1.0", "-2.0"]

    ret = resolver.solve(expression="x^2+3x+2=0")
    assert ret == ["-1.0", "-2.0"]

    ret = resolver.solve(expression="x ^2 + x + 1 = 0")
    assert ret == "No solution in real number."

    ret = resolver.solve(expression="4x ^2 + 4x + 1 = 0")
    assert ret == "-0.5"

    ret = resolver.solve(expression="-x ^2 + 2x - 3 = 0")
    assert ret == "No solution in real number."

    ret = resolver.solve(expression="x ^2 + 4x = 0")
    assert ret == ["0.0", "-4.0"]

    ret = resolver.solve(expression="x ^2 -2x + 1 = 0")
    assert ret == "1.0"

    ret = resolver.solve(expression="x ^ 2 + 1= 0")
    assert ret == "No solution in real number."

    ret = resolver.solve(expression="x^2 -4x + 4 -1= 0")
    assert ret == ["3.0", "1.0"]


def test_equations_infinite_solution():
    resolver = ExpressionResolver(verbose=False)

    # Numbers only
    ret = resolver.solve(expression="2 = 2")
    assert ret == "X can be any real number."

    # Float only
    ret = resolver.solve(expression="2.2456 = 2.2456")
    assert ret == "X can be any real number."


def test_wrong_equation():
    resolver = ExpressionResolver(verbose=False)

    # Numbers only false
    ret = resolver.solve(expression="2 = -2")
    assert ret == "The equation is False."

    # Numbers with var^0 false
    ret = resolver.solve(expression="2*X^0 = -2*X^0")
    assert ret == "There is no solution for this equation."

    # Float only false
    ret = resolver.solve(expression="2.2456 = -2.2456")
    assert ret == "The equation is False."

    # power var with negative value
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="2 = -2X^-5")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    # power var with negative value
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="2 = -2X^(-5)")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    # power var with irational value
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="2 = -2X^5.00000005")
    assert str(e.value) == "irrational numbers are not accepted as exponent."

    # power var with negative irrational value
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="2 = -2X^-5.00000005")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    # power var with negative irrational value
    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="2 = -2X^((-5.00000005))")
    assert str(e.value) == "Some part of the polynomial var have negative power."

    with pytest.raises(NotImplementedError) as e:
        ret = resolver.solve(expression="x^3 + 2x^2 -3x = 0")
    assert (
        str(e.value)
        == "The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
    )
