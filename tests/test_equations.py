# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_equations.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:30 by mabouce           #+#    #+#              #
#    Updated: 2021/01/19 13:47:29 by mabouce          ###   ########.fr        #
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

    ret = resolver.solve(expression="-0x^2 - -X^1  -0X^0    =0")
    assert ret == "0.0"

    # Multiplier small after var
    ret = resolver.solve(expression=" X*0.001=0.000001")
    assert ret == "0.001"

    ret = resolver.solve(expression=" X*0.001=-0.000001")
    assert ret == "-0.001"

    ret = resolver.solve(expression="5 * X^0 = 4 * X^0 + 7 * X^1")
    assert ret == "0.14285714285714285"


def test_equation_degree_two():
    resolver = ExpressionResolver(verbose=False)

    ret = resolver.solve(expression="x^2+x-2 = 0")
    assert ret == ["1.0", "-2.0"]

    ret = resolver.solve(expression="x^2+3x+2=0")
    assert ret == ["-1.0", "-2.0"]

    ret = resolver.solve(expression="x ^2 + x + 1 = 0")
    assert ret == ["-0.5+0.866026*i", "-0.5-0.866026*i"]

    ret = resolver.solve(expression="4x ^2 + 4x + 1 = 0")
    assert ret == "-0.5"

    ret = resolver.solve(expression="-x ^2 + 2x - 3 = 0")
    assert ret == ["1.0-1.414214*i", "1.0+1.414214*i"]

    ret = resolver.solve(expression="x ^2 + 4x = 0")
    assert ret == ["0.0", "-4.0"]

    ret = resolver.solve(expression="x ^2 -2x + 1 = 0")
    assert ret == "1.0"

    ret = resolver.solve(expression="x ^ 2 + 1= 0")
    assert ret == ["i", "-i"]

    ret = resolver.solve(expression="x^2 -4x + 4 -1= 0")
    assert ret == ["3.0", "1.0"]

    ret = resolver.solve(expression="X ^ 2 + X ^1 + x ^2 = 0")
    assert ret == ["0.0", "-0.5"]

    ret = resolver.solve(expression="X ^ 2 + X ^1 - x ^2 = 0")
    assert ret == "0.0"

    ret = resolver.solve(expression="-X ^ 2 + X ^1 + x ^2 = 0")
    assert ret == "0.0"

    ret = resolver.solve(expression="-X ^ 2 + X ^1 - x ^2 = 0")
    assert ret == ["0.0", "0.5"]

    ret = resolver.solve(expression="X ^ 2 + X ^1 + x ^1 = 0")
    assert ret == ["0.0", "-2.0"]

    ret = resolver.solve(expression="X ^ 2 - X ^1 + x ^1 = 0")
    assert ret == "0.0"

    ret = resolver.solve(expression="X ^ 2 - X ^1 - x ^1 = 0")
    assert ret == ["0.0", "2.0"]

    # 0 coeff
    ret = resolver.solve(expression="0x^2    =0")
    assert ret == "X can be any real number."

    ret = resolver.solve(expression="0x^2 * X^1 10X^0    =0")
    assert ret == "X can be any real number."

    ret = resolver.solve(expression="0x^2 * X^1  + 10X^0    =0")
    assert ret == "There is no solution for this equation."

    ret = resolver.solve(expression="0x^2 + X^1  + 10X^0    =0")
    assert ret == "-10.0"

    ret = resolver.solve(expression="-0x^2 + X^1  + 10X^0    =0")
    assert ret == "-10.0"

    ret = resolver.solve(expression="-0x^2 - X^1  + 10X^0    =0")
    assert ret == "10.0"

    ret = resolver.solve(expression="-x^2 - 0X^1  + 10X^0    =0")
    assert ret == ["-3.162278", "3.162278"]

    ret = resolver.solve(expression="-x^2 - -0X^1  + 10X^0    =0")
    assert ret == ["-3.162278", "3.162278"]

    ret = resolver.solve(expression="-x^2 - -0X^1  -0X^0    =0")
    assert ret == "0.0"

    ret = resolver.solve(expression="-0x^2 - -0X^1  -0X^0    =0")
    assert ret == "X can be any real number."

    # positive discriminant
    ret = resolver.solve(expression="5 * X^0 + 13 * X^1 + 3 * X^2 = 1 * X^0 + 1 * X^1")
    assert ret == ["-0.367007", "-3.632993"]

    # Zero discriminant
    ret = resolver.solve(expression="6 * X^0 + 11 * X^1 + 5 * X^2 = 1 * X^0 + 1 * X^1")
    assert ret == "-1.0"

    # Negative discriminant
    ret = resolver.solve(expression="5 * X^0 + 3 * X^1 + 3 * X^2 = 1 * X^0 + 0 * X^1")
    assert ret == ["-0.5+1.040833*i", "-0.5-1.040833*i"]


def test_equations_infinite_solution():
    resolver = ExpressionResolver(verbose=False)

    # Numbers only
    ret = resolver.solve(expression="2 = 2")
    assert ret == "X can be any real number."

    ret = resolver.solve(expression="5 * X^0 = 5 * X^0")
    assert ret == "X can be any real number."

    ret = resolver.solve(expression="4 * X^0 = 8")
    assert ret == "There is no solution for this equation."

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

    # power var with irrational value
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

    # Nothing left
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression=" =0")
    assert str(e.value) == "The equation is not well formated. No left or right part."
